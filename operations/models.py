from __future__ import unicode_literals

from django.db import models
from infrastructure.models import *
import datetime

class Program(models.Model):
    YOUTH_PROGRAM = 'YP'
    CODE = {
        'Youth Program':YOUTH_PROGRAM,
    }
    PROGRAM_TYPE_CHOICES = tuple([(CODE[choice], choice) for choice in ['Youth Program']])
    program_type = models.CharField(max_length=2, choices=PROGRAM_TYPE_CHOICES)
    name = models.CharField(max_length=30)
    group_capacity = models.IntegerField()
    arrival_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    departure_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    def __str__(self):
        return self.name

class Group(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='groups')
    number = models.IntegerField()
    def __str__(self):
        return str(self.program)+' ('+str(self.number)+')'

class Guest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='guests')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    def __str__(self):
        return str(self.group) +' -- ' +self.last_name + ', ' + self.first_name

class Schedule(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False, default=datetime.datetime.now, unique=True)
    models.FileField(upload_to='documents/')
