from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid

from admin_site import settings
from django_unixdatetimefield import UnixDateTimeField


class HasTime(models.Model):
    class Meta:
        abstract = True

    updated = UnixDateTimeField(auto_now=True)


class Compensation(HasTime):
    """
    data model for compensation information
    """

    class Meta:
        db_table = 'profile_compensation'
        # unique_together = ("amount", "duration")

    compensation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.IntegerField(default=0, null=True)
    duration = models.CharField(max_length=200, null=True)


class Profile(HasTime):
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        db_table = 'profile'

    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('profile name'), max_length=200)
    description = models.CharField(_('description'), max_length=200, null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=10, null=True, blank=True)
    compensation = models.ForeignKey(
        Compensation,
        on_delete=models.SET_NULL,
        db_column='compensation_id',
        null=True,
        blank=True,
    )


class Skill(HasTime):
    class Meta:
        db_table = 'profile_skill'

    skill_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skill = models.CharField(max_length=200)


class SkillId(HasTime):
    class Meta:
        db_table = 'profile_skill_id'

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_column='profile_id'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        db_column='skill_id'
    )
