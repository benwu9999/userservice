from __future__ import unicode_literals
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email, RegexValidator
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    data model for User
    """

    # validators
    phoneValidator = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number format: '+999999999'. Max 15# allowed.")

    firstName = models.CharField(_('first name'), max_length=30, null=True, blank=True)
    lastName = models.CharField(_('last name'), max_length=30, null=True, blank=True)
    userId = models.CharField(_('user name'), max_length=30, unique=True)
    email = models.EmailField(_('email address'), validators=[validate_email, ])
    phone = models.CharField(validators=[phoneValidator, ], max_length=15, null=True, blank=True)
    profileIds = models.TextField(null=True, blank=True)
    activeProfileId = models.CharField(max_length=32, null=True, blank=True)
    locationIds = models.TextField(null=True, blank=True)
    activeLocationId = models.CharField(max_length=32, null=True, blank=True)
    applicationIds = models.TextField(null=True, blank=True)
    roles = models.TextField(null=True, blank=True)
    active = models.BooleanField(_('active'), default=True)
    dateJoined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the firstName plus the lastName, with a space in between.
        """
        full_name = '%s %s' % (self.firstName, self.lastName)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user
        """
        return self.firstName

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
