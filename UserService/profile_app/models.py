from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid

from django_unixdatetimefield import UnixDateTimeField
import datetime
import dateutil.parser


class Compensation(models.Model):
    """
    data model for compensation information
    """

    class Meta:
        db_table = 'profile_compensation'
        # unique_together = ("amount", "duration")

    compensation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.IntegerField(default=0, null=True)
    duration = models.CharField(max_length=200, null=True)
    created = UnixDateTimeField()

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.created = dateutil.parser.parse(self.created)
        super(Compensation, self).save()


class Profile(models.Model):
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        db_table = 'profile'

    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('profile name'), max_length=200)
    description = models.CharField(_('description'), max_length=200, null=True, blank=True)
    email = models.EmailField(_('email'), null=True, blank=True)
    other_contact = models.CharField(_('other_contact'), max_length=100, null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=10, null=True, blank=True)
    compensation = models.ForeignKey(
        Compensation,
        on_delete=models.SET_NULL,
        db_column='compensation_id',
        null=True
    )
    created = UnixDateTimeField()
    modified = UnixDateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.created = dateutil.parser.parse(self.created)
        super(Profile, self).save()


class Skill(models.Model):
    class Meta:
        db_table = 'profile_skill'

    skill_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skill = models.CharField(max_length=200)
    created = UnixDateTimeField()

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.created = dateutil.parser.parse(self.created)
        super(Skill, self).save()


class SkillId(models.Model):
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
    created = UnixDateTimeField()

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        else:
            self.created = dateutil.parser.parse(self.created)
        super(SkillId, self).save()
