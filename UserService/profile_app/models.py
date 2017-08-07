from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid

from admin_site import settings


class Compensation(models.Model):
    """
    data model for compensation information
    """

    class Meta:
        db_table = 'compensation'
        # unique_together = ("amount", "duration")

    compensation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.IntegerField(default=0, null=True)
    duration = models.CharField(max_length=200, null=True)


class Profile(models.Model):
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('profile name'), max_length=200)
    description = models.CharField(_('description'), max_length=200)
    phone = models.CharField(_('phone'), max_length=10)
    skills = models.CharField(_('list of skills'), max_length=45)
    compensation = models.ForeignKey(
        Compensation,
        on_delete=models.SET_NULL,
        related_name='compensation',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        db_table = 'profile'
