import itertools

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.http import Http404, HttpResponse, HttpRequest


from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import (
            Field, Account, Match, Slot,
            City, District, Photo, ActivateEmailRequest
            )

from utils.jsonencoder import JSONEncoder

from .serializers import (
            FieldSerializer, MatchSerializer,
            SlotSerializer, CitySerializer,
            DistrictSerializer, AccountSerializer
            )

from .forms import RegisterForm, LoginEmailForm, LoginUsernameForm
from .exceptions import *



def get_access_token(user):
    rtn = Token.objects.get_or_create(user_id=user.id)
    return rtn[0]

def _login_normal(request):
    error = None
    email_or_username = request.REQUEST.get("username", "") or request.REQUEST.get("email", "")

    if "@" in email_or_username:
        post = {k:request.REQUEST[k] for k in request.REQUEST}
        post['email'] = email_or_username
        post['username'] = email_or_username
        form = LoginEmailForm(post)
    else:
        form = LoginUsernameForm(request.REQUEST)
        print form

    if form.is_valid():
        data = form.cleaned_data
        email_or_username = data.get('email') or data.get("username")
        print email_or_username

        try:
            account = Account.objects.login(string_id=email_or_username, password=data['password'], request=request, remember=data['remember'])
        except AccountMissingError:
            error = "Username or email not found."
        except AccountLoginError:
            error = "Invalid password."
        except AccountNoPasswordError:
            error = "Please login using Facebook since you have last logged in using Facebook."
        else:
            pass

    else:
        error = form.errors

    return {
        "form"      : form,
        "error"     : error,
        "email_or_username" : email_or_username,
    }

@csrf_exempt
def register(request):

    """
    For method GET, return the token
    For method POST, create new account base on the input from user and return message
    """

    error = None
    msg = None
    form = RegisterForm()
    is_post = False
    success = False

    if request.method == "POST":
        is_post = True
        form = RegisterForm(request.REQUEST)
        account_dict = {}
        if form.is_valid():
            data = form.cleaned_data

            try:
                account = Account.objects.create_user(
                    email=data['email'],
                    first_name=data['first_name'],
                    password=data['password'],
                    username=data['username'],
                    district_id=data['district_id']
                )
            except AccountEmailTakenError:
                error = "The email has been taken."
            except AccountUsernameTakenError:
                error = "The username has been taken."
            else:

                token = ActivateEmailRequest.objects.generate(account)

                success = True
                msg = "Create new user successfully"
                account_dict = {
                    "id"        : account.id,
                    "name"      : account.first_name,
                    "email"     : account.email,
                    "username"  : account.username,
                }
        else:
            error = "Form is not valid"
        resp = {
            "error"             : error,
            "msg"               : msg,
            "errors"            : form.errors,
            "ok"                : success,
            "account"           : account_dict,
        }
    else:
        resp = {
            "csrf_token"             : get_token(request),
        }
    return HttpResponse(JSONEncoder().encode(resp), content_type="application/json")

@csrf_exempt
def login(request, output='json'):

    result = {}
    msg = None
    error = None
    code = None
    user = None
    rtn = None
    rtn_error = None
    if request.method == "POST":

        firsttime = False
        access_token = None

        rtn = _login_normal(request)

        if rtn and rtn['error'] or rtn_error:
            ok = False
            error = rtn['error'] if rtn else rtn_error
            if rtn and 'code' in rtn and rtn['code']:
                code = rtn['code']
            else:
                code = 400
        else:
            if request.user.is_authenticated():
                ok = True
                # Get access token
                access_token = get_access_token(request.user)
                print request.user
                user = AccountSerializer(request.user).data
                print user
                if user:
                    print here
                    user['access_token'] = access_token.key if access_token else None
                    print user['access_token']
                    user['email'] = request.user.email
            else:
                ok = False
                user = {}
                error = 'Not logged in yet'

        # Response JSON or HTML
        if output == 'json':
            # Generate access token for user

            msg = error
            status = 200 if ok else 401
            resp = {
                'ok'                : ok,
                'user'              : user or None,
                'msg'               : msg,
                'error'             : error,
                'code'              : code,
                'firsttime'         : firsttime,
                'access_token'      : access_token.key if access_token else None,
            }
            return HttpResponse(JSONEncoder().encode(resp), content_type='application/json', status=status)
        elif output == 'html':
            context = {
                "error"             : error,
                "form"              : rtn.get('form') or LoginUsernameForm(),
                "is_post"           : True,
            }
            return render(request, 'api/html/account_login.html', context)

    elif request.method == "GET":
        is_authenticated = request.user.is_authenticated()
        if is_authenticated:
            user = AccountSerializer(request.user).data
            if user:
                access_token = get_access_token(request.user)
                user['access_token'] = access_token.key if access_token else None
                user['email'] = request.user.email
                user['conversion_rate']  = request.user.get_currency_rate()
                if user['is_business']:
                    try:
                        business_acc = Business.objects.get(account=request.user)
                    except Business.DoesNotExist:
                        pass
                    else:
                        user['service_auto_create_place'] = Business.SERVICES_AUTO_CREATE_PLACE
                        user['business_type'] = business_acc.business_type

        # Response JSON or HTML
        if output == 'json':
            status = 200 if is_authenticated else 403
            resp = {
                "csrf_token"        : get_token(request),
                "is_authenticated"  : is_authenticated,
                "user"              : user,
            }
            return HttpResponse(JSONEncoder().encode(resp), content_type='application/json', status=status)
        elif output == 'html':
            context = {
                "error"             : None,
                "form"              : LoginUsernameForm(),
                "is_post"           : False,
            }
            return render(request, 'api/html/account_login.html', context)
    else:
        code = 405
        error = "Method Not Allowed"
        resp = {
            'ok': error == None,
            'detail': error or msg,
        }

        return HttpResponse(JSONEncoder().encode(resp), status=code, content_type="application/json")

@csrf_exempt
def logout(request):
    """
    This view helps user logout and return the form for login again.
    """

    if request.user.is_authenticated():
        _mp.track(request.user.id, 'Logout')

    Account.objects.logout(request)
    resp = {
        'ok': True
    }

    return HttpResponse(JSONEncoder().encode(resp), content_type="application/json")


class FieldList(generics.ListAPIView,
               generics.GenericAPIView):

    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def get(self, request, *args, **kwargs):
        # if request.GET.get('lat') and request.GET.get('lng'):
            
        return self.list(request, *args, **kwargs)

class FieldListViewSet(viewsets.ModelViewSet):

    def list(self, request):
        queryset = list(itertools.chain(Field.objects.all(), Photo.objects.all()))
        serializer = FieldSerializer(queryset, many=True)
        return Response(serializer.data)

class FieldDetail(generics.RetrieveAPIView):

    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class MatchList(generics.ListCreateAPIView):

    queryset            = Match.objects.all()
    serializer_class    = MatchSerializer

    def get(self, request, *args, **kwargs):
        
        # all_field_id = Field.objects.all().values_list('id', flat=True)
        # for field_id in all_field_id:
        #     loca
        self.queryset = self.queryset.all().order_by('-created')
        query_data = MatchSerializer(self.queryset, many=True)
        try:
            ls = self.list(request, *args, **kwargs)
        except Exception as e:
            resp = {
                'detail': 'Invalid params',
                'errors': [str(e)]
            }
            return Response(resp, status=400)
        else:
            return ls

class MatchDetail(generics.RetrieveAPIView):

    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class SlotList(generics.ListAPIView):

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class SlotDetail(generics.RetrieveAPIView):

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)