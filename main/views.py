import itertools
from datetime import datetime

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
            City, District, Photo, ActivateEmailRequest, Comment
            )

from utils.jsonencoder import JSONEncoder, MultiRenderersAPIView

from .serializers import (
            FieldSerializer, MatchSerializer,
            SlotSerializer, CitySerializer,
            DistrictSerializer, AccountSerializer, CommentSerializer
            )


from .forms import RegisterForm, LoginEmailForm, LoginUsernameForm
from .exceptions import *



def get_access_token(user):
    rtn = Token.objects.get_or_create(user_id=user.id)
    return rtn[0]

def _login_normal(request):
    error = None
    email_or_username = request.GET.get("username", "") or request.GET.get("email", "")
    print "-----------------"
    print request.GET.get("password")

    if "@" in email_or_username:
        post = {k:request.GET[k] for k in request.GET}
        post['email'] = email_or_username
        post['username'] = email_or_username
        form = LoginEmailForm(post)
        print form
    else:
        form = LoginUsernameForm(request.GET)
        # print form

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
                    email           =data['email'],
                    first_name      =data['first_name'],
                    password        =data['password'],
                    username        =data['username'],
                    district_id     =data['district_id'],
                    gender          =data['gender'],
                    phone_number    =data['phone_number'],
                    last_name       =data['last_name']
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
                    "id"                : account.id,
                    "name"              : account.first_name,
                    "email"             : account.email,
                    "username"          : account.username,
                    "phone_number"      : account.phone_number,
                    "gender"            : account.gender,
                    "last_name"         : account.last_name,
                    "verification_code" :account.verification_code
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
                user = AccountSerializer(request.user).data
                if user:
                    user['access_token'] = access_token.key if access_token else None
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

    else:
        code = 405
        error = "Method Not Allowed"
        resp = {
            'ok': error == None,
            'detail': error or msg,
        }

        return HttpResponse(JSONEncoder().encode(resp), status=code, content_type="application/json")

# @csrf_exempt
# def logout(request):
#     """
#     This view helps user logout and return the form for login again.
#     """

#     if request.user.is_authenticated():
#         _mp.track(request.user.id, 'Logout')

#     Account.objects.logout(request)
#     resp = {
#         'ok': True
#     }

#     return HttpResponse(JSONEncoder().encode(resp), content_type="application/json")


class AccountView(generics.ListCreateAPIView):

    queryset = Account.objects.filter(is_staff=False, is_superuser=False)
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):            
        return self.list(request, *args, **kwargs)


class AccountDetail(generics.RetrieveAPIView):
    queryset = queryset = Account.objects.filter(is_staff=False, is_superuser=False)
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class FieldList(generics.ListAPIView,
               generics.GenericAPIView):

    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def get(self, request, *args, **kwargs):            
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

class MatchList(generics.ListCreateAPIView,
                        MultiRenderersAPIView):

    queryset            = Match.objects.all()
    serializer_class    = MatchSerializer


    def get(self, request, *args, **kwargs):
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

    def post(self, request, *args, **kwargs):
            get_access_token = None
            try:
                get_access_token = request.META.get('HTTP_AUTHORIZATION')
            except:
                raise Http404
            else:
                error = None
                status_code = None
                field_id             = request.GET.get('field_id')
                maximum_players      = request.GET.get('maximum_players')
                start_time           = request.GET.get('start_time')
                end_time             = request.GET.get('end_time')
                price                = request.GET.get('price')
                sub_match            = request.GET.get('sub_match')
                if get_access_token:
                    get_access_token = get_access_token.split(' ')[1]
                    get_access_token = get_access_token.split("'")[0]
                    user_id = Token.objects.get(key=get_access_token).user_id
                    user_id = Account.objects.get(id=user_id)
                    start_time = datetime.strptime(start_time, '%b %d %Y %I:%M%p')
                    end_time  = datetime.strptime(end_time, '%b %d %Y %I:%M%p')
                    field_instance = Field.objects.get(id=field_id)

                    Match.objects.create(field_id=field_instance,maximum_players=maximum_players,
                                start_time=start_time,end_time=end_time,price=price, host_id=user_id, sub_match=sub_match)
                    status_code = 200
                    error = "Match has been create successfully"
                else:
                    error = 'Missing get_access_token'
                    status_code = 400
                resp = {
                    'detail': error,
                    'status': status_code
                }
            return HttpResponse(JSONEncoder().encode(resp), status=status_code, content_type="application/json")            


class MatchDetail(generics.RetrieveAPIView):

    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class SlotList(generics.ListCreateAPIView,
                MultiRenderersAPIView):

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_access_token = None
        try:
            get_access_token = request.META.get('HTTP_AUTHORIZATION')
        except:
            raise Http404
        else:
            error = None
            status_code = None
            match_id             = request.GET.get('match_id')
            verification_code    = request.GET.get('verification_code')
            if get_access_token:
                get_access_token = get_access_token.split(' ')[1]
                get_access_token = get_access_token.split("'")[0]
                user_id = Token.objects.get(key=get_access_token).user_id
                user_id = Account.objects.get(id=user_id)
                match_id = Match.objects.get(id=match_id)
                Slot.objects.create(verification_code=verification_code,match_id=match_id,user_id=user_id)
                status_code = 200
                error = "success"
            else:
                error = 'Missing get_access_token'
                status_code = 400
            resp = {
                'detail': error,
                'status': status_code
            }
        return HttpResponse(JSONEncoder().encode(resp), status=status_code, content_type="application/json")


class SlotDetail(generics.RetrieveAPIView):

    queryset = Slot.objects.all()
    serializer_class = SlotSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class CommentList(generics.ListCreateAPIView,
                  MultiRenderersAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get(self, request, *args, **kwargs):
        object_id    = request.GET.get('object_id')
        if object_id:
            self.queryset = self.queryset.filter(match_object_id=object_id)
        else:
            self.queryset = self.queryset.none()
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        error = None
        status_code = None
        if request.user.is_authenticated():
            object_id    = request.DATA.get('object_id')
            if object_id:
                request.DATA['object_id']           = object_id
                request.DATA['user']                = request.user.id
                return self.create(request, *args, **kwargs)
            else:
                error = 'Missing object id'
                status_code = 400
        else:
            error = 'No permission'
            status_code = 403
        resp = {
            'detail': error,
            'status': status_code
        }
        return HttpResponse(JSONEncoder().encode(resp), status=status_code, content_type="application/json")
