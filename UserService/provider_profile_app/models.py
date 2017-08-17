from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid

from django_unixdatetimefield import UnixDateTimeField


class ProviderProfile(models.Model):
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(_('company name'), max_length=200)
    description = models.CharField(_('description'), null=True, blank=True, max_length=200)
    phone = models.CharField(_('phone'), max_length=10, null=True, blank=True)
    email = models.EmailField(_('email'), null=True, blank=True)
    other_contact = models.CharField(_('other_contact'), max_length=100, null=True, blank=True)

    created = UnixDateTimeField()
    modified = UnixDateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('provider profile')
        verbose_name_plural = _('provider profiles')
        db_table = 'provider_profile'


class Benefit(models.Model):
    class Meta:
        db_table = 'provider_benefit'

    benefit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    benefit = models.CharField(max_length=200)
    created = UnixDateTimeField(auto_now=True)


class BenefitId(models.Model):
    class Meta:
        db_table = 'provider_benefit_id'

    profile = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        db_column='profile_id'
    )
    benefit = models.ForeignKey(
        Benefit,
        on_delete=models.CASCADE,
        db_column='benefit_id'
    )
    created = UnixDateTimeField(auto_now=True)