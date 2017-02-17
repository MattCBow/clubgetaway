'''----------------------------------------------------------------------------
                    Matthew Bowyer Account Generator
----------------------------------------------------------------------------'''
from django.contrib.auth.models import User
from operations.models import *
from infrastructure.models import *
import random
import numpy as np
import time

class UserTester():
    first_names = [
        'Emma', 'Noah', 'Olivia', 'Liam', 'Sophia', 'Mason', 'Ava	Jacob',
        'Isabella', 'William', 'Mia', 'Ethan', 'Abigail', 'James', 'Emily',
        'Alexander', 'Charlotte', 'Michael', 'Harper', 'Benjamin', 'Madison',
        'Elijah', 'Amelia', 'Daniel', 'Elizabeth', 'Aiden', 'Sofia', 'Logan',
        'Evelyn', 'Matthew', 'Avery', 'Lucas', 'Chloe', 'Jackson', 'Ella',
        'David', 'Grace', 'Oliver', 'Victoria', 'Jayden', 'Aubrey', 'Joseph',
        'Scarlett', 'Gabriel', 'Zoey', 'Samuel', 'Addison', 'Carter', 'Lily',
        'Anthony', 'Lillian', 'John', 'Natalie', 'Dylan', 'Hannah', 'Luke',
        'Aria', 'Henry', 'Layla', 'Andrew', 'Brooklyn', 'Isaac', 'Alexa',
        'Christopher', 'Zoe', 'Joshua', 'Penelope', 'Wyatt', 'Riley',
        'Sebastian', 'Leah', 'Owen', 'Audrey', 'Caleb', 'Savannah', 'Nathan',
        'Allison', 'Ryan', 'Samantha', 'Jack', 'Nora', 'Hunter', 'Skylar',
        'Levi', 'Camila', 'Christian', 'Anna', 'Jaxon', 'Paisley', 'Julian',
        'Ariana', 'Landon', 'Ellie', 'Grayson', 'Aaliyah', 'Jonathan', 'Claire',
        'Isaiah', 'Violet', 'Charles'
    ]

    last_names = [
        'Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller',
        'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White',
        'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson',
        'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen',
        'Young', 'Hernandez', 'King', 'Wright', 'Lopez', 'Hill', 'Scott',
        'Green', 'Adams', 'Baker', 'Gonzalez', 'Nelson', 'Carter', 'Mitchell',
        'Perez', 'Roberts', 'Turner', 'Phillips', 'Campbell', 'Parker', 'Evans',
        'Edwards', 'Collins', 'Stewart', 'Sanchez', 'Morris', 'Rogers', 'Reed',
        'Cook', 'Morgan', 'Bell', 'Murphy', 'Bailey', 'Rivera', 'Cooper',
        'Richardson', 'Cox', 'Howard', 'Ward', 'Torres', 'Peterson', 'Gray',
        'Ramirez', 'James', 'Watson', 'Brooks', 'Kelly', 'Sanders', 'Price',
        'Bennett', 'Wood', 'Barnes', 'Ross', 'Henderson', 'Coleman', 'Jenkins',
        'Perry', 'Powell', 'Long', 'Patterson', 'Hughes', 'Flores',
        'Washington', 'Butler', 'Simmons', 'Foster', 'Gonzales', 'Bryant',
        'Alexander', 'Russell', 'Griffin', 'Diaz', 'Hayes'
    ]
    def generate_user(self):
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        self.create_user(first_name, last_name)

    def create_user(self,first_name, last_name):
        done = False
        attempt = 1
        while not done:
            try:
                username = (last_name+first_name+str(attempt)).lower()
                password = (first_name+'password').lower()
                user = User.objects.create_user(username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                done = True
                print 'Created User Cridentials => '+username+':'+password
            except IntegrityError as e:
                attempt += 1

    def generate_names(self, num_of_names):
        names = []
        for i in range(num_of_names):
            name = {}
            name['first'] = random.choice(self.first_names)
            name['last'] = random.choice(self.last_names)
            names.append(name)
        return names


    def create_program(self, program_type, program_name, group_capacity, start_date, end_date, guest_names):
        program = Program(
            name=program_name,
            program_type=program_type,
            group_capacity=group_capacity,
            start_date=start_date,
            end_date=end_date
        )
        program.save()
        num_of_groups = (len(guest_names)/group_capacity)+1
        for group_id in range(num_of_groups):
            group = Group(
                program=program,
                number=(group_id+1)
            )
            group.save()
            for name in guest_names[group_id::num_of_groups]:
                guest = Guest(
                    group=group,
                    first_name=name['first'],
                    last_name=name['last']
                )
                guest.save()

    def generate_program(self, program_type, program_name, group_capacity, start_date, end_date, number_of_guests):
        return self.create_program(
            program_type=program_type,
            program_name=program_name,
            group_capacity=group_capacity,
            start_date=start_date,
            end_date=end_date,
            guest_names=self.generate_names(number_of_guests)
        )

'''
from scheduler.generator import *
from operations.models import *
test = UserTester()
test.generate_program(
    program_type=Program.CODE['Youth Program'],
    program_name='My First Program',
    group_capacity=25,
    start_date='2017-01-01',
    end_date='2017-01-02',
    number_of_guests=100
)
'''

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

def print_schedule(schedule, zones):
    nickname = {
        'Adventure Woods' : 'Adventure Woods\t',
        'Adventure Base Camp' :'Adventure Base Camp',
        'Waterside Village' :'Waterside Village',
        'Waterside Tent' :'Waterside Tent\t',
        'The Plateau' :'The Plateau\t',
        'Waterfront' :'Waterfront\t',
        'White Tent' :'White Tent\t',
        'The Valley':'The Valley\t',
        'Moose Lodge Area' :'Moose Lodge Area\t',
        'Mountain View Field' :'Mountain View Field',
    }

    visitors = {zone:[0 for p in range(len(schedule))] for zone in zones}
    for p in range(len(schedule)):
        for g in range(len(schedule[0])):
            z = schedule[p][g]
            visitors[z][p] += 1

    for period in range(len(schedule)):
        print '\t\t\tPERIOD: [', str(1+period), ']',
    for group in range(len(schedule[0])):
        print '\nGROUP: [', str(group), ']\t',
        for period in range(len(schedule)):
            z = schedule[period][group]
            print ('['+str(visitors[z][p])+'/'+str(int(zones[z]['capacity']))+']'), nickname[z], '\t',
    print '\n'

def create_schedule(periods, groups, choices):
    keys = choices.keys()
    schedule = [[ 'White Tent' for group in range(groups)] for period in range(periods)]
    factors = [[ None for group in range(groups)] for period in range(periods)]
    period = 0
    group = 0
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
                if (time.time() - start_time) > 60:
                    schedule = [[ 'White Tent' for group in range(groups)] for period in range(periods)]
                    factors = [[ None for group in range(groups)] for period in range(periods)]
                    period = 0
                    group = 0
                    start_time = time.time()
                print 'BACKWARD\t['+str(len(attempts))+']\t'+str(attempt[300:])
            p = [(factors[period][group][key]['hueristic']/t) for key in keys]
            schedule[period][group] = keys[np.random.choice(range(len(p)), p=p)]
            group += 1
        period += 1
    print_schedule(schedule, choices)
    return schedule


'''
#[PERIOD][GROUP]
from scheduler.scheduler import *
choices = format_choices(Zone.objects.all())
s = create_schedule(5,60, choices)


Assigment = {
    Period = int,
    Group = int,
    Zone = key,
    Prev Assignment = {self},
    Next Assignment = {self},
    Potential Next = [self...]
}

'''
