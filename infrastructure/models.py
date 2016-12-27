from __future__ import unicode_literals

from django.db import models


class ProgramType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Period(models.Model):
    start = models.TimeField()
    next_period = models.ForeignKey('self', blank=True, null=True)

    def __str__(self):
        return self.start.__str__()

class Activity(models.Model):
    name = models.CharField(max_length=30, unique=True)
    capacity = models.IntegerField()
    activity_level = models.IntegerField(blank=True, null=True)
    availability = models.ManyToManyField(Period, blank=True,)

    def __str__(self):
        return self.name + ' (' + str(self.capacity) + ')'

class Zone(models.Model):
    name = models.CharField(max_length=30)
    activities = models.ManyToManyField(Activity, blank=True)
    adjacent_zones = models.ManyToManyField('self', blank=True)

    def get_capacity(self):
        capacity = 0
        for activity in self.activities.all():
            capacity += activity.capacity

    def __str__(self):
        capacity = self.get_capacity()
        return self.name + ' (' + str(capacity) + ')'
