from django.db import models
from infrastructure.models import *
from operations.models import *
from django.contrib.auth.models import User


class Schedule(models.Model):
    day = models.DateField(auto_now=False, auto_now_add=False, unique=True)
    def __str__(self):
        return self.day.__str__()

class Assigment(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='assignments')
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    def __str__(self):
        return group.__str__() + ' <--> ' + activity.__str__() + ' <--> ' + Period.__str__()

class GroupLeader(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='group_leaders')
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    def __str__(self):
        return leader.__str__() + ' <--> ' + group.__str__()

class Floater(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='floaters')
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    def __str__(self):
        return floater.__str__() + ' <--> ' + activity.__str__()
