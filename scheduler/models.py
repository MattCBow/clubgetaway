from django.db import models
from infrastructure import models as infrastructure_models
from operations import models as operations_models

class GroupLeader(models.Model):
    leader = models.OneToOneField(operations_models.Employee, blank=False)
    group = models.OneToOneField(operations_models.Group, blank=False)
    def __str__(self):
        return leader.__str__() + ' <--> ' + group.__str__()

class Floater(models.Model):
    floater = models.OneToOneField(operations_models.Employee, blank=False)
    activity = models.OneToOneField(infrastructure_models.Activity, blank=False)
    def __str__(self):
        return floater.__str__() + ' <--> ' + activity.__str__()

class Assigment(models.Model):
    group = models.OneToOneField(operations_models.Group, blank=False)
    activity = models.OneToOneField(infrastructure_models.Activity, blank=False)
    period = models.OneToOneField(infrastructure_models.Period, blank=False)
    def __str__(self):
        return group.__str__() + ' <--> ' + activity.__str__() + ' <--> ' + Period.__str__()

class Schedule(models.Model):
    day = models.DateField(auto_now=False, auto_now_add=False, unique=True)
    assignments = models.ManyToManyField(Assigment, blank=False)
    def __str__(self):
        return self.day.__str__()
