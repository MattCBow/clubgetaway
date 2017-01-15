'''----------------------------------------------------------------------------
                    Matthew Bowyer Account Generator
----------------------------------------------------------------------------'''
from django.contrib.auth.models import User
from operations.models import *
from infrastructure.models import *
import random

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

def floydwarshall(graph):

    # Initialize dist and pred:
    # copy graph into dist, but add infinite where there is
    # no edge, and 0 in the diagonal
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
        # given dist u to v, check if path u - t - v is shorter
        for u in graph:
            for v in graph:
                newdist = dist[u][t] + dist[t][v]
                if newdist < dist[u][v]:
                    dist[u][v] = newdist
                    pred[u][v] = pred[t][v] # route new path through t

    return dist



def hueristic(schedule, period, group, zone):
    visits = 0.0
    for prev_period in range(period):
        if schedule[prev_period][group]['assigment'] is zone:
            visits += 1
    p_vists = visits/period
    visitors = 0.0
    for prev_group in range(group):
        if schedule[period][prev_group]['assigment'] is zone:
            visitors += 1
    p_visitors = visitors/zone['capacity']
    distance = 1
    if period is not 0
        distance = distance[zone['name']][schedule[period-1][group]['assigment']['name']]
    factors = {}
    factor['level'] = (zone['activity_level'])
    factor['distance'] = zone['distance-to'][schedule[period-1][group]['name']]
    factor['visits'] = (1-p_visits)
    factor['visitors'] = (1-p_visitors)
    return (1.0)*factor['activity'] + (1.0)*factor['distance'] + (1.0)*factor['visits'] + (1.0)*factor['visitors']



def create_schedule(periods, groups, zones):
    schedule = [[{'assignmnet':None, 'hueristic':None} for group in range(groups)] for period in range(periods)]
    for period in range(periods):
        for group in range(groups):

            if schedule[period][group]['hueristic'] is None:
                schedule[period][group]['hueristic'] = [hueristic(schedule, period, group, zone) for zone in zones]

            #Backtrack if out of possibilities
            if sum(schedule[period][group]['hueristic']) is 0:
                if group is 0:
                    period -=1
                else
                    group -=1

            #Make probability distribution equal to  1
            p = schedule[period][group]['hueristic'] / sum(schedule[period][group]['hueristic']))
            schedule[period][group]['assignmnet'] = np.random.choice(zones, p)
    return schedule



'''
import numpy as np

Periods = integer
Groups = integer
Zones = [{'name':(...), 'capacity':(...), 'weight':(...) 'adjacent_zones':(...)} for zone in zones]
Assigment = {'zone_assigned':(...), 'probabilities':{zone1:p1, zone2:p2, ... zoneN:pN}}


zones = [{'name':zone} for zone in range(10)]
np.random.choice(zones, p=[1.0/len(zones) for zone in zones])

graph = {0 : {1:6, 2:8},
         1 : {4:11},
         2 : {3: 9},
         3 : {},
         4 : {5:3},
         5 : {2: 7, 3:4}}

dist, pred = floydwarshall(graph)
print 'Predecesors in shortest path:'
for v in pred:
    print '%s: %s' % (v, pred[v])
print 'Shortest distance from each vertex:'
for v in dist:
    print '%s: %s' % (v, dist[v])

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


from infrastructure.models import *
zone_query = Zone.objects.all()

zones = []
graph = {}

for zone in zone_query:
    z = {}
    z['name'] = zone.name
    z['capacity'] = 0
    z['level'] = 0
    for activity in zone.activities.all():
        z['capacity'] += activity.capacity
        z['level'] += activity.level * activity.capacity
    z['level'] /= z['capacity']
    graph[zone.name]={neighbor.name : 1  for neighbor in zone.adjacent_zones}
    zones += z



'''
