from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid

class ProviderProfile(models.Model):

    profileId=models.UUIDField(primary_key=True, default=uuid.uuid5, editable=False)
    companyName=models.CharField(_('company name'), max_length=200)
    description=models.CharField(_('description'), max_length=200)
    phone=models.CharField(_('phone'), max_length=10)
    email=models.EmailField(_('email'))
    benefits=models.CharField(_('list of benefits'), max_length=45)
    active=models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('provider profile')
        verbose_name_plural = _('provider profiles')