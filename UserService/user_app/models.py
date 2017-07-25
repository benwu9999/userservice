from __future__ import unicode_literals
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email, RegexValidator
from .managers import UserManager
from django.conf import settings
import uuid

# fields in model will use camel case so django can parse json which is also camel case

class AbstractMapping(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column = 'user_id'
    )
    class Meta:
        abstract = True

class ProfileId(AbstractMapping):
    profile_id = models.CharField(primary_key=True, max_length=200)
    class Meta:
        db_table = 'profile_id'

class ProviderProfileId(AbstractMapping):
    provider_profile_id = models.CharField(primary_key=True, max_length=200)
    class Meta:
        db_table = 'provider_profile_id'

class ApplicationId(AbstractMapping):
    application_id = models.CharField(primary_key=True, max_length=200)
    class Meta:
        db_table = 'application_id'

class LocationId(AbstractMapping):
    location_id = models.CharField(primary_key=True, max_length=200)
    class Meta:
        db_table = 'location_id'

class JobPostId(AbstractMapping):
    job_post_id = models.CharField(primary_key=True, max_length=200)
    class Meta:
        db_table = 'job_post_id'

class Role(AbstractMapping):
    role = models.CharField(null=True, blank=True, max_length=200)
    class Meta:
        db_table = 'role'

class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'user'
    # validators
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number format: '+999999999'. Max 15# allowed.")
    user_id = models.CharField(primary_key=True, max_length=40, null=False, blank=False)
    first_name = models.CharField(_('first name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, null=True, blank=True)
    email = models.EmailField(_('email address'), validators=[validate_email, ])
    phone = models.CharField(validators=[phone_validator, ], max_length=15, null=True, blank=True)
    # not considering provider profile for now, assume all users are seekers
    active_profile_id = models.ForeignKey(
        ProfileId,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True, null=True,
    )
    active_provider_profile_id = models.ForeignKey(
        ProviderProfileId,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True, null=True,
    )
    active_location_id = models.ForeignKey(
        LocationId,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True, null=True,
    )
    active = models.BooleanField(_('active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email']