from __future__ import unicode_literals

from django.db import models
from infrastructure import models as infrastructure_models

class Program(models.Model):
    program_type = models.ForeignKey(infrastructure_models.ProgramType, related_name='programs')
    name = models.CharField(max_length=30)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    def __str__(self):
        return self.name

class Group(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='groups')
    number = models.IntegerField()
    def __str__(self):
        return str(self.program)+' ('+str(number)+')'

class Guest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='guests')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    def __str__(self):
        return str(self.group) +' -- ' +self.last_name + ', ' + self.first_name

class Abscence(models.Model):
    day = models.DateField(auto_now=False, auto_now_add=False, unique=True)
    employee = models.ManyToManyField(infrastructure_models.Employee, blank=True)
    activity = models.ManyToManyField(infrastructure_models.Activity, blank=True)
    def __str__(self):
        return self.day.__str__()
