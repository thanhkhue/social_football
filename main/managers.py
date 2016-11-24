
import uuid
import datetime
from django.utils import importlib

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import authenticate, login as auth_login

from .exceptions import *

from django.utils import importlib

OLD_SESSION_KEY = 'old_sessionid'

_models = importlib.import_module('main.models')

def social_login(request, user):
    ''' Log in and store old session id key '''
    old_session_id = request.session.session_key
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    rtn = auth_login(request, user)
    request.session[OLD_SESSION_KEY] = old_session_id
    return rtn

class ActionRequestManager(models.Manager):
    # Subclass should override these.
    TYPE = None
    EXPIRES_SECONDS = None

    def _get_prehash(self, account):
        """Subclass should override this."""

        raise NotImplementedError()

    def __get_hashed(self, account, token):
        from django.utils.crypto import salted_hmac

        contents = str(account.id) + self._get_prehash(account)

        return salted_hmac(token, contents).hexdigest()

    def generate(self, account):
        # TODO: implement throttling

        type    = self.TYPE
        now     = timezone.now()
        expiry  = now + datetime.timedelta(seconds=self.EXPIRES_SECONDS)
        token   = uuid.uuid4().hex
        hashed  = self.__get_hashed(account, token)

        try:
            request = self.create(
                account=account,
                type=type,
                hashed=hashed,
                expiry=expiry,
            )
        except IntegrityError:
            self.filter(account=account, type=type).update(hashed=hashed, expiry=expiry)

        return token

    def verify(self, account, token):
        """
        Checks whether a token is valid.
        :returns: bool -- True if OK.
        """

        type = self.TYPE

        try:
            request = self.get(account=account, type=type)
        except self.model.DoesNotExist:
            return False

        now = timezone.now()
        hashed = self.__get_hashed(account, token)

        if now < request.expiry and request.hashed == hashed:
            return True

        return False

    def destroy(self, account):
        self.filter(account=account, type=self.TYPE).delete()

class ActivateEmailRequestManager(ActionRequestManager):
    TYPE = 1 # TODO: prevent circular import _models.ActionRequest.TYPE_ACTIVATE_EMAIL
    EXPIRES_SECONDS = 3600 * 24 * 30 # 30 days in seconds

    def to_utf8(self, s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    def _get_prehash(self, account):
        return self.to_utf8(account.email.lower())

class AccountManager(BaseUserManager):
    @classmethod
    def normalize_email(cls, email):
        email = email or '' # follow BaseUserManager's behavior

        return email.lower()

    @classmethod
    def normalize_username(cls, username):
        return username.lower()

    def _set_login(self, account, request, remember):
        if remember:
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        else:
            # 0 means expire on browser exit
            request.session.set_expiry(0)

        social_login(request, account)


    def login(self, string_id, password, request, remember=True):

        if ("@" in string_id):
            email = self.normalize_email(string_id)

            account = _models.Account.objects.get(email=email)
        else:
            username = self.normalize_username(string_id)
            account = _models.Account.objects.get(username=username)

        if account:

            self._set_login(account=account, request=request, remember=remember)

            return account

        raise AccountLoginError()

    def logout(self, request):
        """Logs out the user and destroys all session data.

        :returns:   void
        """

        fiuzu_logout(request)


    def __init_account(self, email, first_name, username, is_superuser, district_id, phone_number, gender, last_name):
        if not email:
            raise ValueError('Email must be set.')

        if not username:
            raise ValueError("Username must be set.")

        account = self.model(
            email=email,
            first_name=first_name,
            username=username,
            is_staff=is_superuser,
            is_active=is_superuser,
            is_superuser=is_superuser,
            district_id=district_id,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number,
        )

        return account

    def __create_user(self, email, first_name, password, is_superuser,district_id, phone_number, last_name, gender, username=None):
        account = self.__init_account(email=email, first_name=first_name,
                                    is_superuser=is_superuser,
                                    district_id=district_id, phone_number=phone_number,
                                    gender=gender, last_name=last_name , username=username)
        account.set_password(password)
        account.full_clean(validate_unique=False)
        email = account.email # get cleaned email

        try:
            account.save()
        except IntegrityError as e:
            # Check whether it is the email or username that is taken.
            if self.filter(email=email).count():
                raise AccountEmailTakenError(cause=e)

            raise AccountUsernameTakenError(cause=e)

        return account

    def create_random_password(self):
        l = settings.DEFAULT_RANDOM_PASSWORD_LENGTH
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(l))
        return password

    def create_user(self, email, first_name, password, district_id, phone_number, last_name, gender,  username=None):
        return self.__create_user(email, first_name, password, False,district_id, phone_number, last_name, gender, username)