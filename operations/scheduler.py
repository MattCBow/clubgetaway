'''----------------------------------------------------------------------------
                    Matthew Bowyer Account Generator
----------------------------------------------------------------------------'''

from os.path import join
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from infrastructure.models import *
from .models import *
import datetime
import random
import numpy
import csv

class Printer():
    def print_structure(structure, depth):
        ret = ""
        if structure is None:
            ret += '\n'
        if isinstance(structure, type('a')):
            ret += ('\t'*depth) + (structure) + ('\n')
        if isinstance(structure, type(1)):
            ret += ('\t'*depth) + (str(structure)) + ('\n')
        if isinstance(structure, type(1.0)):
            ret += ('\t'*depth) + (str(structure)) + ('\n')
        if isinstance(structure, type((1,2))):
            ret += ('\t'*depth) + str(structure[0]) + (": ") + print_structure(structure[1], depth)[depth:]
        if isinstance(structure, type([])):
            ret += ('\t'*depth) + ('[') + ('\n')
            for i in range(0,len(structure)): ret += print_structure((i,structure[i]), depth+1)
            ret = ret[:len(ret)-1] + (']') + ('\n')
        if isinstance(structure, type({})) and len(structure):
            ret += ('\t'*depth) + ('{') + ('\n')
            for (k,v) in structure.iteritems(): ret += print_structure((k,v), depth+1)
            ret = ret[:len(ret)-1] + ('}') + ('\n')
        return ret

    def print_struct(structure):
        print print_structure(structure, 0)


class Scheduler():



def create_csv_example():
    with open('schedule2.0.csv', 'wb') as csvfile:
        employees = [{'last': 'Cooper', 'first': 'Jack'}, {'last': 'James', 'first': 'William'}, {'last': 'Morris', 'first': 'Charles'}, {'last': 'Powell', 'first': 'Daniel'}, {'last': 'Phillips', 'first': 'Mason'}, {'last': 'Evans', 'first': 'Aiden'}, {'last': 'Powell', 'first': 'Samantha'}, {'last': 'Mitchell', 'first': 'Christian'}, {'last': 'Clark', 'first': 'Jack'}, {'last': 'Cox', 'first': 'Carter'}, {'last': 'Carter', 'first': 'Lillian'}, {'last': 'Lopez', 'first': 'Allison'}, {'last': 'Rogers', 'first': 'Gabriel'}, {'last': 'Bennett', 'first': 'Landon'}, {'last': 'Hernandez', 'first': 'Harper'}, {'last': 'Rivera', 'first': 'Grayson'}, {'last': 'Adams', 'first': 'Grayson'}, {'last': 'Hernandez', 'first': 'Samantha'}, {'last': 'Lopez', 'first': 'Michael'}, {'last': 'Parker', 'first': 'Ella'}, {'last': 'Young', 'first': 'Benjamin'}, {'last': 'Anderson', 'first': 'Dylan'}, {'last': 'Griffin', 'first': 'Skylar'}, {'last': 'Bennett', 'first': 'Natalie'}, {'last': 'Patterson', 'first': 'Benjamin'}, {'last': 'Murphy', 'first': 'Joseph'}, {'last': 'Robinson', 'first': 'Samantha'}, {'last': 'Kelly', 'first': 'Leah'}, {'last': 'Lee', 'first': 'Addison'}, {'last': 'Martinez', 'first': 'Michael'}, {'last': 'Hughes', 'first': 'Chloe'}, {'last': 'Hernandez', 'first': 'Elizabeth'}, {'last': 'Ward', 'first': 'Hannah'}, {'last': 'Jones', 'first': 'Gabriel'}, {'last': 'Campbell', 'first': 'Hannah'}, {'last': 'Murphy', 'first': 'Jaxon'}, {'last': 'Clark', 'first': 'Liam'}, {'last': 'Davis', 'first': 'Christopher'}, {'last': 'Lee', 'first': 'Carter'}, {'last': 'Anderson', 'first': 'Lily'}, {'last': 'Powell', 'first': 'Carter'}, {'last': 'Brown', 'first': 'Lily'}, {'last': 'Coleman', 'first': 'Liam'}, {'last': 'Smith', 'first': 'Ryan'}, {'last': 'Gonzalez', 'first': 'Paisley'}, {'last': 'White', 'first': 'Chloe'}, {'last': 'Smith', 'first': 'William'}, {'last': 'White', 'first': 'Levi'}, {'last': 'Phillips', 'first': 'Victoria'}, {'last': 'Torres', 'first': 'Lucas'}, {'last': 'Stewart', 'first': 'Skylar'}, {'last': 'Jones', 'first': 'Abigail'}, {'last': 'Hall', 'first': 'Caleb'}, {'last': 'Peterson', 'first': 'Logan'}, {'last': 'Ramirez', 'first': 'Zoey'}, {'last': 'Wilson', 'first': 'Evelyn'}, {'last': 'Coleman', 'first': 'Elijah'}, {'last': 'Rodriguez', 'first': 'Andrew'}, {'last': 'Barnes', 'first': 'Lillian'}, {'last': 'Ross', 'first': 'Jayden'}, {'last': 'Griffin', 'first': 'Caleb'}, {'last': 'Martinez', 'first': 'Mason'}, {'last': 'Gonzales', 'first': 'James'}, {'last': 'James', 'first': 'Carter'}, {'last': 'Murphy', 'first': 'Alexa'}, {'last': 'Sanchez', 'first': 'Jack'}, {'last': 'Mitchell', 'first': 'Matthew'}, {'last': 'Foster', 'first': 'Violet'}, {'last': 'Bryant', 'first': 'Zoey'}, {'last': 'Anderson', 'first': 'Jayden'}, {'last': 'Garcia', 'first': 'Natalie'}, {'last': 'Clark', 'first': 'Gabriel'}, {'last': 'Diaz', 'first': 'Scarlett'}, {'last': 'Bell', 'first': 'Violet'}, {'last': 'Jackson', 'first': 'Aubrey'}, {'last': 'Flores', 'first': 'Jackson'}, {'last': 'Reed', 'first': 'Nathan'}, {'last': 'Kelly', 'first': 'James'}, {'last': 'Walker', 'first': 'Harper'}, {'last': 'Green', 'first': 'Mason'}, {'last': 'Gray', 'first': 'Jonathan'}, {'last': 'Hall', 'first': 'Dylan'}, {'last': 'Ward', 'first': 'Gabriel'}, {'last': 'Wright', 'first': 'Charles'}, {'last': 'Jones', 'first': 'Mason'}, {'last': 'Alexander', 'first': 'Joshua'}, {'last': 'Washington', 'first': 'Ethan'}, {'last': 'Martin', 'first': 'Victoria'}, {'last': 'Torres', 'first': 'Aria'}, {'last': 'Clark', 'first': 'Charlotte'}, {'last': 'Jenkins', 'first': 'Aiden'}, {'last': 'Cooper', 'first': 'Elijah'}, {'last': 'Sanders', 'first': 'Noah'}, {'last': 'Coleman', 'first': 'James'}, {'last': 'Carter', 'first': 'Skylar'}, {'last': 'Bailey', 'first': 'Natalie'}, {'last': 'Washington', 'first': 'Alexa'}, {'last': 'Bryant', 'first': 'Isabella'}, {'last': 'Johnson', 'first': 'William'}, {'last': 'Davis', 'first': 'Ethan'}]
        schedule = [['Arrival', 'Moose Lodge Area', 'Waterside Tent', 'Waterfront', 'Mountain View Field', 'Adventure Base Camp'], ['Arrival', 'The Plateau', 'Waterfront', 'The Valley', 'Adventure Base Camp', 'Mountain View Field'], ['Arrival', 'Waterfront', 'The Valley', 'The Plateau', 'Mountain View Field', 'Adventure Base Camp'], ['Arrival', 'Waterfront', 'Waterside Village', 'Adventure Woods', 'The Plateau', 'Adventure Base Camp'], ['Arrival', 'Moose Lodge Area', 'Adventure Woods', 'Waterside Village', 'Waterside Tent', 'The Plateau'], ['Arrival', 'Adventure Base Camp', 'Waterside Tent', 'Mountain View Field', 'Waterside Village', 'Moose Lodge Area'], ['Arrival', 'The Plateau', 'Waterside Tent', 'The Valley', 'Moose Lodge Area', 'Waterfront'], ['Arrival', 'Waterside Village', 'The Plateau', 'The Valley', 'Waterside Tent', 'Adventure Base Camp'], ['Arrival', 'Waterside Tent', 'Mountain View Field', 'Adventure Base Camp', 'The Valley', 'Waterside Village'], ['Arrival', 'Mountain View Field', 'Adventure Woods', 'Waterside Village', 'The Valley', 'Waterfront'], ['Arrival', 'Adventure Base Camp', 'Adventure Woods', 'Mountain View Field', 'Waterside Tent', 'Waterfront'], ['Arrival', 'Waterside Tent', 'The Plateau', 'Adventure Base Camp', 'The Valley', 'Mountain View Field'], ['Arrival', 'Waterfront', 'The Valley', 'Moose Lodge Area', 'Adventure Base Camp', 'Waterside Tent'], ['Arrival', 'Adventure Base Camp', 'Adventure Woods', 'Waterside Village', 'Waterside Tent', 'Waterfront'], ['Arrival', 'Waterside Village', 'Adventure Woods', 'Waterfront', 'Waterside Tent', 'The Valley'], ['Arrival', 'The Valley', 'The Plateau', 'Moose Lodge Area', 'Mountain View Field', 'Waterfront'], ['Arrival', 'Waterfront', 'Waterside Tent', 'The Plateau', 'Adventure Woods', 'Moose Lodge Area'], ['Arrival', 'Mountain View Field', 'Waterside Tent', 'Adventure Woods', 'Moose Lodge Area', 'The Plateau'], ['Arrival', 'Adventure Woods', 'Mountain View Field', 'Waterside Tent', 'The Plateau', 'Waterside Village'], ['Arrival', 'Waterside Tent', 'Adventure Base Camp', 'The Plateau', 'Moose Lodge Area', 'The Valley'], ['Arrival', 'Adventure Woods', 'Waterfront', 'The Valley', 'Waterside Village', 'Mountain View Field'], ['Arrival', 'Adventure Base Camp', 'Waterside Tent', 'Mountain View Field', 'The Valley', 'Moose Lodge Area'], ['Arrival', 'Mountain View Field', 'Adventure Base Camp', 'Adventure Woods', 'The Plateau', 'Waterside Village'], ['Arrival', 'Waterside Village', 'The Plateau', 'Adventure Base Camp', 'Waterfront', 'Moose Lodge Area'], ['Arrival', 'The Plateau', 'Adventure Woods', 'The Valley', 'Mountain View Field', 'Waterside Village'], ['Arrival', 'Moose Lodge Area', 'The Valley', 'Waterside Village', 'The Plateau', 'Adventure Woods'], ['Arrival', 'Adventure Woods', 'Waterside Village', 'Adventure Base Camp', 'Moose Lodge Area', 'Waterside Tent'], ['Arrival', 'The Plateau', 'Waterside Tent', 'Moose Lodge Area', 'Waterside Village', 'Adventure Base Camp'], ['Arrival', 'Waterfront', 'Adventure Base Camp', 'Adventure Woods', 'Waterside Village', 'The Valley'], ['Arrival', 'Waterside Village', 'Waterfront', 'The Valley', 'Moose Lodge Area', 'Adventure Woods'], ['Arrival', 'Adventure Base Camp', 'The Valley', 'Adventure Woods', 'Moose Lodge Area', 'The Plateau'], ['Arrival', 'Adventure Base Camp', 'Moose Lodge Area', 'Mountain View Field', 'Adventure Woods', 'The Plateau'], ['Arrival', 'Moose Lodge Area', 'Mountain View Field', 'Waterfront', 'Waterside Tent', 'The Valley'], ['Arrival', 'The Plateau', 'Waterfront', 'Waterside Tent', 'Mountain View Field', 'Moose Lodge Area'], ['Arrival', 'The Plateau', 'Waterfront', 'Mountain View Field', 'Adventure Base Camp', 'Waterside Village'], ['Arrival', 'Moose Lodge Area', 'The Valley', 'Mountain View Field', 'Adventure Base Camp', 'Adventure Woods'], ['Arrival', 'Waterside Village', 'The Valley', 'Waterside Tent', 'The Plateau', 'Moose Lodge Area'], ['Arrival', 'Adventure Base Camp', 'Waterside Tent', 'Waterfront', 'The Valley', 'Adventure Woods'], ['Arrival', 'Mountain View Field', 'Moose Lodge Area', 'Adventure Base Camp', 'Waterside Village', 'The Valley'], ['Arrival', 'Waterside Village', 'Adventure Woods', 'Adventure Base Camp', 'The Plateau', 'Waterside Tent'], ['Arrival', 'The Plateau', 'Waterside Village', 'Waterfront', 'Waterside Tent', 'Moose Lodge Area'], ['Arrival', 'Moose Lodge Area', 'Mountain View Field', 'The Plateau', 'Adventure Woods', 'The Valley'], ['Arrival', 'Adventure Base Camp', 'The Valley', 'Mountain View Field', 'Adventure Woods', 'Waterside Village'], ['Arrival', 'Adventure Woods', 'Moose Lodge Area', 'The Valley', 'Waterfront', 'Adventure Base Camp'], ['Arrival', 'Mountain View Field', 'Adventure Base Camp', 'Adventure Woods', 'The Valley', 'Waterside Tent'], ['Arrival', 'Mountain View Field', 'Adventure Base Camp', 'Waterside Tent', 'The Valley', 'Adventure Woods'], ['Arrival', 'Waterside Tent', 'The Plateau', 'Adventure Woods', 'Moose Lodge Area', 'Mountain View Field'], ['Arrival', 'Mountain View Field', 'Adventure Base Camp', 'Moose Lodge Area', 'The Plateau', 'Waterside Tent'], ['Arrival', 'Moose Lodge Area', 'Mountain View Field', 'The Plateau', 'Adventure Base Camp', 'Waterside Tent'], ['Arrival', 'Adventure Woods', 'Adventure Base Camp', 'Moose Lodge Area', 'The Valley', 'Mountain View Field'], ['Arrival', 'The Valley', 'Adventure Woods', 'Mountain View Field', 'Adventure Base Camp', 'Waterside Tent'], ['Arrival', 'The Valley', 'Moose Lodge Area', 'Waterside Village', 'Mountain View Field', 'The Plateau'], ['Arrival', 'Adventure Woods', 'Waterside Village', 'Moose Lodge Area', 'Mountain View Field', 'The Valley'], ['Arrival', 'Adventure Woods', 'The Valley', 'Waterside Tent', 'Adventure Base Camp', 'Mountain View Field'], ['Arrival', 'Waterside Tent', 'Adventure Base Camp', 'Waterside Village', 'Mountain View Field', 'The Plateau'], ['Arrival', 'Adventure Woods', 'The Plateau', 'Adventure Base Camp', 'Mountain View Field', 'Waterside Tent'], ['Arrival', 'Mountain View Field', 'Waterside Village', 'Waterside Tent', 'Adventure Woods', 'The Valley'], ['Arrival', 'The Valley', 'The Plateau', 'Moose Lodge Area', 'Adventure Woods', 'Mountain View Field'], ['Arrival', 'Waterside Tent', 'Mountain View Field', 'The Plateau', 'Waterside Village', 'The Valley'], ['Arrival', 'Mountain View Field', 'Waterside Village', 'The Plateau', 'Waterfront', 'Adventure Base Camp']]
        schedule_date = '3/10/2017'
        prefered_lunch = '14:00'
        first_period = '9:30'
        period_length = 90
        schedule_writer = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        periods = len(schedule[0])
        month = int(schedule_date[:schedule_date.index('/')])
        day = int(schedule_date[schedule_date.index('/')+1:schedule_date.index('/',2)])
        year = int(schedule_date[schedule_date.index('/',2)+1:])
        hrs = int(first_period[:first_period.index(':')])
        mins = int(first_period[first_period.index(':')+1:])
        date = datetime.datetime(year,month,day,hrs,mins,0)
        time_display = [str(date.date()),'',] + [ (date+datetime.timedelta(minutes=(p*period_length))).strftime("%I:%M %p") for p in range(periods)]
        employee_assignments = numpy.random.choice(employees, len(schedule))
        schedule_writer.writerow(time_display)
        for group_id in range(len(schedule)):
            group_name = 'Group ('+str(group_id)+')'
            employee_name = employee_assignments[group_id]['last']+', '+employee_assignments[group_id]['first']
            group_assignment_display = [employee_name,group_name]+schedule[group_id]
            schedule_writer.writerow(group_assignment_display)


def create_csv(name):
    gls = User.objects.filter(groups__name='GroupLeaders')
    num_of_groups = (len(guest_names)/group_capacity)+1

    path = join(settings.MEDIA_ROOT, name)
    with open(path, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=str(u','), quotechar=str(u'\"'), quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(('col1'))
        for num in range(3):
            csv_writer.writerow([num, 'hi'])


'''

#[PERIOD][GROUP]
choices = format_choices(Zone.objects.all())
s = create_schedule(5,60, choices)
test = ScheduleTester()
test.generate_program(
    program_type=Program.CODE['Youth Program'],
    program_name='My First Program',
    group_capacity=25,
    start_date='2017-01-01',
    end_date='2017-01-02',
    number_of_guests=100
)


Assigment = {
    Period = int,
    Group = int,
    Zone = key,
    Prev Assignment = {self},
    Next Assignment = {self},
    Potential Next = [self...]
}


from django.contrib.auth.models import User
from django.contrib.auth.models import Group
employees = User.objects.filter(groups__name='GroupLeaders')

import datetime
from operations.scheduler import ScheduleTester
ScheduleTester().generate_programs(10, datetime.datetime.now().date())

'''
