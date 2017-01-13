from django.db import models
from infrastructure import models as infrastructure_models
from operations import models as operations_models


class Schedule(models.Model):
    day = models.DateField(auto_now=False, auto_now_add=False, unique=True)
    def __str__(self):
        return self.day.__str__()

class Assigment(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    period = models.ForeignKey(infrastructure_models.Period, on_delete=models.CASCADE)
    group = models.ForeignKey(operations_models.Group, on_delete=models.CASCADE)
    activity = models.ForeignKey(infrastructure_models.Activity, on_delete=models.CASCADE)
    def __str__(self):
        return group.__str__() + ' <--> ' + activity.__str__() + ' <--> ' + Period.__str__()

class GroupLeader(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    employee = models.ForeignKey(operations_models.Employee, on_delete=models.CASCADE)
    group = models.ForeignKey(operations_models.Group, on_delete=models.CASCADE)
    def __str__(self):
        return leader.__str__() + ' <--> ' + group.__str__()

class Floater(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    employee = models.ForeignKey(operations_models.Employee, on_delete=models.CASCADE)
    activity = models.ForeignKey(infrastructure_models.Activity, on_delete=models.CASCADE)
    def __str__(self):
        return floater.__str__() + ' <--> ' + activity.__str__()
