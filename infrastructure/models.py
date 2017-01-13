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
    def __str__(self):
        return self.name + ' (' + str(self.capacity) + ')' + ' --- ' + str(self.zone)

class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    qualifications = models.ManyToManyField(Activity, blank=True)
    def __str__(self):
        return self.last_name + ', ' + self.first_name
