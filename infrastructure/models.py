from __future__ import unicode_literals

from django.db import models


class ProgramType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    group_capacity = models.IntegerField()
    def __str__(self):
        return self.name

class Period(models.Model):
    start = models.TimeField()
    next_period = models.ForeignKey('self', blank=True, null=True)
    def __str__(self):
        return self.start.__str__()

class Zone(models.Model):
    name = models.CharField(max_length=30)
    adjacent_zones = models.ManyToManyField('self', blank=True)
    def __str__(self):
        capacity = self.get_capacity()
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=30, unique=True)
    capacity = models.IntegerField()
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    activity_level = models.IntegerField(blank=True, null=True)
    availability = models.ManyToManyField(Period, blank=True,)
    def __str__(self):
        return self.name + ' (' + str(self.capacity) + ')'
