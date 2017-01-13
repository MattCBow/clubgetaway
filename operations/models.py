from __future__ import unicode_literals

from django.db import models
from infrastructure import models as infrastructure_models


class Guest(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    def __str__(self):
        return self.last_name + ', ' + self.first_name

class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    qualifications = models.ManyToManyField(infrastructure_models.Activity, blank=True)
    def __str__(self):
        return self.last_name + ', ' + self.first_name

class Program(models.Model):
    name = models.CharField(max_length=30)
    program_type = models.ForeignKey(infrastructure_models.ProgramType, related_name='programs')
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    guests = models.ManyToManyField(Guest, blank=True)
    def __str__(self):
        return self.name

class Group(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=30)
    guests = models.ManyToManyField(Guest, blank=True)
    def __str__(self):
        return self.name

class Abscence(models.Model):
    day = models.DateField(auto_now=False, auto_now_add=False, unique=True)
    employee = models.ManyToManyField(Employee, blank=True)
    activity = models.ManyToManyField(infrastructure_models.Activity, blank=True)
    def __str__(self):
        return self.day.__str__()
