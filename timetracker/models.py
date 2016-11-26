from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from colorful.fields import RGBColorField
from autoslug import AutoSlugField


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=20, null=False, blank=False)

    def regenerate_token(self):
        pass

    def __str__(self):
        return "UserData for {}: token={}".format(self.user, self.token)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False, blank=False)
    slug = AutoSlugField(populate_from="name", null=False, blank=False)
    subtraction = models.IntegerField(blank=False, null=False, default=0)
    count_multiple = models.BooleanField(blank=False, null=False, default=False)
    allow_day_crossing = models.BooleanField(blank=False, null=False, default=False)
    color = RGBColorField(blank=False, null=False, default="#87BBFF")
    comment = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{} ({}, {})".format(self.name, self.comment, self.slug)


class Span(models.Model):
    task = models.ForeignKey(Task, blank=False, null=False)
    comment = models.CharField(max_length=100, blank=True, null=True)
    start = models.DateTimeField(blank=False, null=False, default=timezone.now)
    end = models.DateTimeField(null=True)

    def has_ended(self):
        return self.end is not None

    @property
    def duration(self):
        if self.start is None or self.end is None:
            return 0

        duration_delta = self.end - self.start
        seconds = duration_delta.total_seconds()
        minutes = seconds / 60  # yes, fractional minutes are lost here

        return minutes

    def __str__(self):
        return "{} from {} to {}".format(self.task.name, self.start, self.end)