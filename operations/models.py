from __future__ import unicode_literals

import csv
import datetime

from django.db import models
from infrastructure.models import *
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
    campers = models.PositiveIntegerField(default=0)
    day = models.DateField(auto_now=True)
    arrival_time = models.ForeignKey(Period,on_delete=models.SET_NULL, null=True, related_name='arriving_group')
    departure_time = models.ForeignKey(Period,on_delete=models.SET_NULL, null=True, related_name='departing_group')
    def __str__(self):
        return self.name+' -- '+str(self.day)

class Schedule(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False, default=datetime.datetime.now, unique=True)
    lunch = models.ForeignKey(Period,on_delete=models.SET_NULL,blank=True, null=True, related_name='scheduled_lunch')
    dinner = models.ForeignKey(Period,on_delete=models.SET_NULL,blank=True, null=True, related_name='scheduled_dinner')
    absence = models.ManyToManyField(User,blank=True)
    csv = models.FileField(upload_to='schedules/',blank=True)
    def save(self, *args, **kwargs):
        if self.csv.name == '':
            create_csv(self.date)
            self.csv.name='schedules/'+str(self.date)+'.csv'
        super(Schedule, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.date)

'''
-------------------------Scheduler--------------------------------
'''
def floydwarshall(graph):
    dist = {}
    pred = {}
    for u in graph:
        dist[u] = {}
        pred[u] = {}
        for v in graph:
            dist[u][v] = 1000
            pred[u][v] = -1
        dist[u][u] = 0
        for neighbor in graph[u]:
            dist[u][neighbor] = graph[u][neighbor]
            pred[u][neighbor] = u
    for t in graph:
        for u in graph:
            for v in graph:
                newdist = dist[u][t] + dist[t][v]
                if newdist < dist[u][v]:
                    dist[u][v] = newdist
                    pred[u][v] = pred[t][v]
    return dist

def format_choices(zone_query):
    zones = {}
    graph = {}
    for zone in zone_query:
        name = zone.name.encode('ascii','ignore')
        zones[name] = {'capacity':0,'level':0}
        zones[name]['capacity'] = 0
        zones[name]['level'] = 0
        for activity in zone.activities.all():
            zones[name]['capacity'] += activity.capacity
            zones[name]['level'] += activity.level * activity.capacity
        zones[name]['capacity'] = (1.0*zones[name]['capacity'])
        zones[name]['level'] = (1.0*zones[name]['level'])/zones[name]['capacity']
        graph[name] = {adjacent_zones.name.encode('ascii','ignore') : 1  for adjacent_zones in zone.adjacent_zones.all()}
    proximity = floydwarshall(graph)
    for name in zones.keys():
        zones[name]['proximity'] = proximity[name]
    return zones

def calculate_factors(period, group, zones, schedule):
    f = {}
    visits = {zone:0.0 for zone in zones.keys()}
    for prev_period in range(period):
        visits[schedule[prev_period][group]] += 1
    visitors = {zone:0.0 for zone in zones.keys()}
    for prev_group in range(group):
        visitors[schedule[period][prev_group]] += 1
    prev_zone = 'White Tent'
    if period > 0:
        prev_zone = schedule[period-1][group]
    for zone in zones.keys():
        f[zone] = {}
        f[zone]['level'] = zones[zone]['level']/5.0
        f[zone]['capacity'] = zones[zone]['capacity']
        f[zone]['visits'] = visits[zone]
        f[zone]['visitors'] = visitors[zone]
        f[zone]['vacancy'] = (1.0*f[zone]['capacity'] - 1.0*f[zone]['visitors']) / f[zone]['capacity']
        f[zone]['proximity'] = 1.0 - 1.0*zones[prev_zone]['proximity'][zone]/5
        f[zone]['hueristic'] = 0.0
        if f[zone]['vacancy'] != 0.0 and f[zone]['visits'] == 0.0 and f[zone]['level'] != 0.0:
            f[zone]['hueristic'] = 1#(10.0*f[zone]['proximity']) + (1.0*f[zone]['vacancy']) + (1.0*f[zone]['level'])
    return f

def create_schedule(periods, groups, choices):
    keys = choices.keys()
    schedule = [[ 'White Tent' for group in range(groups)] for period in range(periods)]
    factors = [[ None for group in range(groups)] for period in range(periods)]
    period = 0
    group = 0
    trial_time = time.time()
    start_time = time.time()
    while period < periods:
        group = 0
        while group < groups:
            if factors[period][group] is None:
                factors[period][group] = calculate_factors(period, group, choices, schedule)
            t = sum([factors[period][group][key]['hueristic'] for key in keys])
            while t == 0.0:
                factors[period][group] = None
                if group is not 0:
                    group -=1
                elif period is not 0:
                    group = groups-1
                    period -=1
                else:
                    print 'NO POSSIBLE SCHEDULES'
                    return schedule, factors
                prev_assignment = schedule[period][group]
                schedule[period][group] = 'White Tent'
                factors[period][group][prev_assignment]['hueristic'] = 0.0
                t = sum([factors[period][group][key]['hueristic'] for key in keys])
                if (time.time() - trial_time) > 60:
                    schedule = [[ 'White Tent' for group in range(groups)] for period in range(periods)]
                    factors = [[ None for group in range(groups)] for period in range(periods)]
                    period = 0
                    group = 0
                    trial_time = time.time()
                if (time.time() - start_time) > 300:
                    print 'NO POSSIBLE SCHEDULES'
                    return schedule, factors
                print 'BACKWARD\t['+str(period)+']['+str(group)+']\t',
            p = [(factors[period][group][key]['hueristic']/t) for key in keys]
            schedule[period][group] = keys[numpy.random.choice(range(len(p)), p=p)]
            group += 1
        period += 1
    return schedule

def create_csv(date):
    path = join(settings.MEDIA_ROOT, 'schedules/'+str(date)+'.csv')
    employees = User.objects.filter(groups__name='GroupLeaders')
    programs = Program.objects.filter(day=date)
    zones = format_choices(Zone.objects.all())
    periods = Period.objects.all()
    groups = []
    for program in programs:
        program_groups = (program.campers/group_capacity)+1
        for i in range(program_groups):
            groups.append(str(program.name)+' ('+str(i+1)+')')
    s = create_schedule(len(periods),total_groups, zones)
    schedule = [list(i) for i in zip(*s)]
    with open(path, 'wb') as csvfile:
        schedule_writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        periods = len(schedule[0])
        time_display = [str(date),'',] + [str(p) for p in periods]
        employee_assignments = numpy.random.choice(employees, len(schedule))
        schedule_writer.writerow(time_display)
        for group_id in range(len(schedule)):
            group_assignment_display = [ str(employees[group_id]), groups[group_id] ]+schedule[group_id]
            schedule_writer.writerow(group_assignment_display)
