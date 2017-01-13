from __future__ import unicode_literals

from django.db import models


class ProgramType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    group_capacity = models.IntegerField()
    def __str__(self):
        return self.name

class Period(models.Model):
    start = models.TimeField()
    next_period = models.ForeignKey('self', blank=True, null=True, related_name='previous_period')
    def __str__(self):
        return self.start.__str__()

class Zone(models.Model):
    name = models.CharField(max_length=30)
    adjacent_zones = models.ManyToManyField('self', blank=True, symmetrical=True)
    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=30, unique=True)
    capacity = models.IntegerField()
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='activities')
    activity_level = models.IntegerField(blank=True, null=True)
    availability = models.ManyToManyField(Period, blank=True,)
    def __str__(self):
        return self.name + ' (' + str(self.capacity) + ')' + ' --- ' + str(self.zone)
