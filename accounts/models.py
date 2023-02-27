from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from .managers import CustomAccountManager
from datetime import datetime, time
from administrator.models import *
from django.utils import timezone
from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Account(AbstractUser):
    ROLES = (
            ('',  _('Select')),
            (1,  _('Administrator')),
            (2, _('Donor')),
    )

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. Between 5 and 150 characters. Letters, digits and @/./+/-/_ only.'),
        validators=[MinLengthValidator(5), UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_('email address'), unique=True)

    role = models.PositiveSmallIntegerField(
        choices=ROLES,
        default=2,
    )

    # Phone number in E.164 formatting for the purpose of sending notification via SMS and WhatsApp
    # The CharField has a max length of 16 characters because the E.164 standard allows a maximum of 15 digits for a number.
    # Fifteen characters include both the country code and the phone number. An additional character is reserved for the + sign,
    # which is the prefix for the country code.
    phone_number = PhoneNumberField(max_length=16, unique=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'role']
    USERNAME_FIELD = 'username'

    objects = CustomAccountManager()
