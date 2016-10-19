from __future__ import unicode_literals

import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator, MinLengthValidator

class City(models.Model):
    name                = models.CharField(max_length=50, blank=True)
    def __unicode__(self):
        return self.name

class District(models.Model):
    district_name       = models.CharField(max_length=50, blank=True)
    city_id             = models.ForeignKey(City, on_delete=models.PROTECT, db_index=False)
    def __unicode__(self):
        return self.district_name


class Account(models.Model):

    GENDER_MALE     = 'm'
    GENDER_FEMALE   = 'f'
    GENDER_CHOICES  = (
        (GENDER_MALE,      _('Male')),
        (GENDER_FEMALE,    _('Female')),
    )

    USERNAME_RE     = re.compile(r"^[a-z0-9_.-]+$", re.I)

    INVALID_TIMEZONE = 32000

    USERNAME_MIN_LENGTH = 5
    PASSWORD_MIN_LENGTH = 6
    PASSWORD_MAX_LENGTH = 30

    TYPE_DEFAULT      = 1
    TYPE_GRAVATAR     = 2
    TYPE_UPLOAD       = 3

    AVATAR_TYPE = (
        (TYPE_DEFAULT,      _('Default')),
        (TYPE_GRAVATAR,     _('Gravatar')),
        (TYPE_UPLOAD,       _('Upload')),
    )


    email = models.EmailField(max_length=75, unique=True, verbose_name=_("Email"))
    username        = models.CharField(max_length=32, unique=True, verbose_name=_("Username"), validators=[RegexValidator(regex=USERNAME_RE),MinLengthValidator(USERNAME_MIN_LENGTH)])
    first_name      = models.CharField(max_length=50, verbose_name=_("First name"))
    middle_name     = models.CharField(max_length=50, blank=True, default='')
    last_name       = models.CharField(max_length=50, blank=True, default='')
    password        = models.CharField(_('password'), max_length=128,help_text=_("Use'[algo]$[salt]$[hexdigest]' or use the <a href=\"password/\">change password form</a>."))
    phone_number    = models.CharField(max_length = 15, validators=[phone_regex], blank=True)
    gender          = models.CharField(max_length=1, blank=True, default='', choices=GENDER_CHOICES)
    birthday        = models.DateField(null=True, blank=True, verbose_name=_("Date of birth"))
    description     = models.CharField(max_length=512, blank=True, default='', verbose_name=_('About'))
    timezone        = models.SmallIntegerField(default=INVALID_TIMEZONE)
    district_id     = models.ForeignKey(District, on_delete=models.PROTECT, db_index=False)

    is_staff        = models.BooleanField(default=False)

    is_active       = models.BooleanField(default=False)

    is_superuser    = models.BooleanField(default=False)

    """Whether the email address is verified."""

    created         = models.DateTimeField(auto_now_add=True, editable=False)


    """ Avatar type """
    avatar_type     = models.PositiveIntegerField(default=1, choices=AVATAR_TYPE)

    '''Deactivate'''
    is_disabled     = models.BooleanField(default=False, verbose_name=_('Is deactivated'))

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name



class Field(models.Model):
    name                = models.CharField(max_length=50, blank=True)
    district_id         = models.ForeignKey(District, on_delete=models.PROTECT, db_index=False)
    address             = models.CharField(max_length=100)
    price_morning       = models.FloatField()
    price_afternoon     = models.FloatField()
    price_evening       = models.FloatField()
    phone_regex         = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number        = models.CharField(max_length = 15, validators=[phone_regex], blank=True)
    photo               = models.ImageField()
    rating              = models.FloatField()
    lat                 = models.DecimalField(max_digits=9, decimal_places=6)
    lng                 = models.DecimalField(max_digits=9, decimal_places=6)
    created             = models.DateTimeField(auto_now_add=True, editable=False)
    deleted             = models.DateTimeField(auto_now_add=True, editable=False)

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

class Slot(models.Model):
    user_id             = models.ForeignKey(Account)
    quantity            = models.SmallIntegerField()
    is_verified         = models.BooleanField(default=False)
    created             = models.DateTimeField(auto_now_add=True, editable=False)
    updated             = models.DateTimeField(auto_now_add=True, editable=False)
    deleted             = models.DateTimeField(auto_now_add=True, editable=False)    
