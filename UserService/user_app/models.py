from __future__ import unicode_literals
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email, RegexValidator
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    from django.db import models
from django.conf import settings
import uuid

class User(AbstractBaseUser, PermissionsMixin):
    # validators
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number format: '+999999999'. Max 15# allowed.")
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_('first name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, null=True, blank=True)
    user_name = models.CharField(_('user id'), max_length=30, unique=True)
    email = models.EmailField(_('email address'), validators=[validate_email, ])
    phone = models.CharField(validators=[phone_validator, ], max_length=15, null=True, blank=True)
    # not considering provider profile for now, assume all users are seekers
    active_profile_id = models.ForeignKey(
        ProfileId,
        on_delete=models.CASCADE,
    )
    active_location_id = models.ForeignKey(
        LocationId,
        on_delete=models.CASCADE,
    )
    roles = models.TextField(null=True, blank=True)
    active = models.BooleanField(_('active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = ['email']


class AbstractMapping(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    class Meta:
        abstract = True


class ProfileId(AbstractMapping):
    profile_id = models.CharField(primary_key=True, max_length=200)


class ProviderProfileId(AbstractMapping):
    provider_profile_id = models.CharField(primary_key=True, max_length=200)


class ApplicationId(AbstractMapping):
    application_id = models.CharField(primary_key=True, max_length=200)


class LocationId(AbstractMapping):
    location_id = models.CharField(primary_key=True, max_length=200)

class JobPostId(AbstractMapping):
    job_post_id = models.CharField(primary_key=True, max_length=200)
