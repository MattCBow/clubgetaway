from __future__ import unicode_literals

import csv
import datetime

from django.db import models
from infrastructure.models import *
from operations.scheduler import *
from django.contrib.auth.models import User

from django.conf import settings
from os.path import join

class Program(models.Model):
    YOUTH_PROGRAM = 'YP'
    CODE = {
        'Youth Program':YOUTH_PROGRAM,
    }
    PROGRAM_TYPE_CHOICES = tuple([(CODE[choice], choice) for choice in ['Youth Program']])
    program_type = models.CharField(max_length=2, choices=PROGRAM_TYPE_CHOICES)
    name = models.CharField(max_length=30)
    campers = models.IntegerField()
    arrival_time = models.ForeignKey(Period,on_delete=models.SET_NULL, null=True, related_name='arriving_group')
    departure_time = models.ForeignKey(Period,on_delete=models.SET_NULL, null=True, related_name='departing_group')
    def __str__(self):
        return self.name

class Schedule(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False, default=datetime.datetime.now, unique=True)
    lunch = models.ForeignKey(Period,on_delete=models.SET_NULL,blank=True, null=True, related_name='scheduled_lunch')
    dinner = models.ForeignKey(Period,on_delete=models.SET_NULL,blank=True, null=True, related_name='scheduled_dinner')
    absence = models.ManyToManyField(User,blank=True)
    csv = models.FileField(upload_to='schedules/',blank=True)
    def save(self, *args, **kwargs):
        if self.csv.name == '':
            path = 'schedules/'+str(self.date)+'.csv'
            create_csv(path)
            self.csv.name=path
        super(Schedule, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.date)

def create_csv(name):
    path = join(settings.MEDIA_ROOT, name)
    Program.objects.filter(date__range=["2011-01-01", "2011-01-31"])


    with open(path, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=str(u','), quotechar=str(u'\"'), quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(('col1'))
        for num in range(3):
            csv_writer.writerow([num, 'hi'])
