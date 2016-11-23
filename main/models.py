from __future__ import unicode_literals

import re
import hashlib
import time

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator, MinLengthValidator, URLValidator
from djbase.models import FixedCharField, BaseModel

from .managers import ActionRequestManager, ActivateEmailRequestManager, AccountManager

DEFAULT_EXAM_ID = 1

def _createHash():
    hash = hashlib.md5()
    hash.update(str(time.time()))
    return  hash.hexdigest()[:-10]

class City(models.Model):
    name                = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return self.name

class District(models.Model):
    district_name       = models.CharField(max_length=50, blank=True)
    city_id             = models.ForeignKey(City, on_delete=models.PROTECT, db_index=False)
    def __unicode__(self):
        return self.district_name

class Account(AbstractBaseUser, BaseModel):

    GENDER_MALE         = 'm'
    GENDER_FEMALE       = 'f'
    GENDER_CHOICES      = (
        (GENDER_MALE,      _('Male')),
        (GENDER_FEMALE,    _('Female')),
    )

    USERNAME_RE         = re.compile(r"^[a-z0-9_.-]+$", re.I)

    INVALID_TIMEZONE    = 32000

    USERNAME_MIN_LENGTH = 5
    PASSWORD_MIN_LENGTH = 6
    PASSWORD_MAX_LENGTH = 30

    email               = models.EmailField(max_length=75, unique=True, verbose_name=_("Email"))
    username            = models.CharField(max_length=32, unique=True, verbose_name=_("Username"), validators=[RegexValidator(regex=USERNAME_RE),MinLengthValidator(USERNAME_MIN_LENGTH)])
    first_name          = models.CharField(max_length=50, verbose_name=_("First name"))
    middle_name         = models.CharField(max_length=50, blank=True, default='')
    last_name           = models.CharField(max_length=50, blank=True, default='')
    phone_regex         = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number        = models.CharField(max_length = 15, validators=[phone_regex], blank=True)
    gender              = models.CharField(max_length=1, blank=True, default='', choices=GENDER_CHOICES)
    birthday            = models.DateField(null=True, blank=True, verbose_name=_("Date of birth"))
    description         = models.CharField(max_length=512, blank=True, default='', verbose_name=_('About'))
    timezone            = models.SmallIntegerField(default=INVALID_TIMEZONE)
    district_id         = models.ForeignKey(District, on_delete=models.PROTECT, db_index=False)
    verification_code   = models.CharField(max_length=100,default=_createHash(),unique=True)
    is_staff            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_superuser        = models.BooleanField(default=False)
    created             = models.DateTimeField(auto_now_add=True, editable=False)
    is_disabled         = models.BooleanField(default=False, verbose_name=_('Is deactivated'))

    objects = AccountManager()
    class Meta:
        db_table = "account"

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


FIVE_SIZE         = '5'
SEVEN_SIZE       = '7'
SIZE_CHOICES      = (
    (FIVE_SIZE,      '5'),
    (SEVEN_SIZE,    '7'),
)

class ActionRequest(BaseModel):
    TYPE_ACTIVATE_EMAIL     = 1
    TYPE_PASSWORD_RESET     = 2
    TYPE_CHOICES = (
        (TYPE_ACTIVATE_EMAIL, "Activate email"),
        (TYPE_PASSWORD_RESET, "Password reset"),
    )

    account     = models.ForeignKey(Account, db_index=False, on_delete=models.CASCADE, related_name="+")
    type        = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    hashed      = FixedCharField(max_length=40)
    expiry      = models.DateTimeField()
    objects     = ActionRequestManager()

    class Meta:
        unique_together = (
            ("account", "type"),
        )


class ActivateEmailRequest(ActionRequest):
    objects     = ActivateEmailRequestManager()

    class Meta:
        proxy = True


class PhotoSize(object):

    def __init__(self, name, width, height, is_fixed=True, quality=75):
        self.name = name
        self.width = width
        self.height = height
        self.is_fixed = is_fixed
        self.quality = quality
        
class Photo(models.Model):

    # SIZES           = {
    #     "xs"    : PhotoSize(name="xs", width= 60,  height= 45,  is_fixed=True,  quality=60),
    #     "ss"    : PhotoSize(name="ss", width=100,  height=100,  is_fixed=True,  quality=70),
    #     "sm"    : PhotoSize(name="sm", width=120,  height= 90,  is_fixed=True,  quality=75),
    #     "md"    : PhotoSize(name="md", width=320,  height=240,  is_fixed=True,  quality=85),
    #     "lg"    : PhotoSize(name="lg", width=800,  height=600,  is_fixed=False, quality=90),
    #     "og"    : PhotoSize(name="og", width=0,    height=0,),
    # }
    source_size_og             = models.URLField(blank=True)
    source_size_lg             = models.URLField(blank=True)
    source_size_md             = models.URLField(blank=True)
    source_size_sm             = models.URLField(blank=True)
    source_size_xs             = models.URLField(blank=True)
    source_size_ss             = models.URLField(blank=True)

class Field(models.Model):
    name                = models.CharField(max_length=50, blank=True)
    district_id         = models.ForeignKey(District, on_delete=models.PROTECT, db_index=False)
    address             = models.CharField(max_length=100)
    price_morning       = models.FloatField()
    price_afternoon     = models.FloatField()
    price_evening       = models.FloatField()
    phone_regex         = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number        = models.CharField(max_length = 15, validators=[phone_regex], blank=True)
    rating              = models.FloatField()
    photo               = models.ForeignKey("Photo", default=DEFAULT_EXAM_ID, related_name='photos')
    lat                 = models.DecimalField(max_digits=9, decimal_places=6)
    lng                 = models.DecimalField(max_digits=9, decimal_places=6)
    created             = models.DateTimeField(auto_now_add=True, editable=False)
    deleted             = models.DateTimeField(auto_now_add=True, editable=False)
    size                = models.CharField(max_length=1, blank=True,choices=SIZE_CHOICES)


    def __unicode__(self):
        return self.name




class Match(models.Model):
    field_id            = models.ForeignKey(Field, on_delete=models.PROTECT, db_index=False)
    host_id             = models.ForeignKey(Account)
    status              = models.SmallIntegerField()
    maximum_players     = models.SmallIntegerField(default=12)
    price               = models.FloatField()
    start_time          = models.DateTimeField()
    end_time            = models.DateTimeField()
    is_verified         = models.BooleanField(default=False)
    created             = models.DateTimeField(auto_now_add=True, editable=False)
    updated             = models.DateTimeField(auto_now_add=True, editable=False)
    deleted             = models.DateTimeField(auto_now_add=True, editable=False)
    def __unicode__(self):
        return "Match of " + self.host_id.first_name.title() + ' in ' + self.field_id.name 

class Slot(models.Model):
    user_id             = models.ForeignKey(Account)
    match_id            = models.ForeignKey(Match)
    quantity            = models.SmallIntegerField()
    is_verified         = models.BooleanField(default=False)
    verification_code   = models.CharField(max_length=10,default=_createHash(),unique=True)
    created             = models.DateTimeField(auto_now_add=True, editable=False)
    updated             = models.DateTimeField(auto_now_add=True, editable=False)
    deleted             = models.DateTimeField(auto_now_add=True, editable=False)