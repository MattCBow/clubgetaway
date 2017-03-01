from __future__ import unicode_literals

from django.db import models


class Period(models.Model):
    start = models.TimeField()
    next_period = models.ForeignKey('self', blank=True, null=True, related_name='previous_period')
    def __str__(self):
        return self.start.strftime("%I:%M %p")

class Zone(models.Model):
    name = models.CharField(max_length=30)
    adjacent_zones = models.ManyToManyField('self', blank=True, symmetrical=True)
    def __str__(self):
        return self.name

class Activity(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=30, unique=True)
    capacity = models.IntegerField()
    level = models.IntegerField()
    def __str__(self):
        return str(self.zone) + ' ----- '+str(self.name) + '('+str(self.capacity) + ') LEVEL ' + str(self.level)
