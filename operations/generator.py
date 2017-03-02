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

class ScheduleTester():
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
    team_names = [
        'The Easy Raccoons', 'The Unwieldy Rhinoceroses', 'The Near Humans',
        'The Uppity Cobras', 'The Black Eels', 'The Necessary Lyrebirds',
        'The Piquant Ravens', 'The Ripe Jackals', 'The Wandering Echidnas',
        'The Stereotyped Coyotes', 'The Soft Llamas', 'The Abrupt Lemurs',
        'The Womanly Toads', 'The Minor Butterflys', 'The Grateful Cats',
        'The Stale Falcons', 'The Thundering Snakes', 'The Right Rams',
        'The Petite Pelicans', 'The Spotty Armadillos', 'The Ubiquitous Pandas',
        'The Bustling Lions', 'The Wry Dogs', 'The Squealing Cranes',
        'The Adhesive Mallards', 'The Hissing Peafowls', 'The Sloppy Mosquitos',
        'The Hanging Otters', 'The Fumbling Goats', 'The Brief Weasels',
        'The Lean Aardvarks', 'The Giant Jaguars', 'The Capricious Swans',
        'The Unique Yaks', 'The Obeisant Beavers', 'The Vacuous Badgers',
        'The Aloof Dragons', 'The Precious Giraffes', 'The Defective Gerbils',
        'The Vast Gorillas', 'The Ahead Herons', 'The Resonant Barracudas',
        'The Three Cows', 'The Tan Gulls', 'The Teeny-tiny Bees',
        'The Resolute Mice', 'The Vengeful Reindeers', 'The Spotless Hawks',
        'The Good Mooses', 'The Childlike Elks', 'The Null Frogs',
        'The Lazy Larks', 'The Animated Apes', 'The Ethereal Seals',
        'The Regular Worms', 'The Dizzy Guineapigs', 'The Medical Panthers',
        'The Disagreeable Hippopotamuss', 'The Stupendous Porcupines',
        'The New Hedgehogs', 'The Purring Crabs', 'The Greasy Bears',
        'The Delirious Moles', 'The Guttural Salamanders', 'The Whole Donkeys',
        'The Scarce Buffalos', 'The Known Elephants', 'The Foamy Squirrels',
        'The Long-term Shrews', 'The Calm Gazelles', 'The Enchanted Antelopes',
        'The Wretched Wolves', 'The Tearful Turtles', 'The Observant Chimpanzees',
        'The Grieving Koalas', 'The Homely Sheep', 'The Plain Eagles',
        'The Brash Dogfishes', 'The Annoyed Hamsters', 'The Demonic Turkeys',
        'The Abnormal Stinkbugs', 'The Nutty Louses', 'The Complex Monkeys',
        'The Faulty Flys', 'The Fanatical Lobsters', 'The Odd Mules',
        'The Organic Jellyfishes', 'The Quarrelsome Walruses',
        'The Zealous Magpies', 'The Ruddy Penguins', 'The Glistening Whales',
        'The Hungry Anteaters', 'The Cloudy Boars', 'The Mighty Finches',
        'The Selfish Dragonflys', 'The Jazzy Pigeons', 'The Absurd Deers',
        'The Worried Leopards', 'The Gifted Antelopes', 'The Standing Wolves',
        'The Outgoing Turtles'
    ]
    activity_names = [
        'Mountain View Field -- Bungee Trampoline (4) LEVEL 5',
        'Mountain View Field -- Aero Ball (1) LEVEL 4',
        'Mountain View Field -- A Mazing Adventure (2) LEVEL 4',
        'Mountain View Field -- Stunt Swing (1) LEVEL 5',
        'Mountain View Field -- Crazy Olympics (4) LEVEL 3',
        'Moose Lodge Area -- Technical Rock Climb (1) LEVEL 4',
        'Moose Lodge Area -- Mountain Hike (4) LEVEL3',
        'Moose Lodge Area -- Photo Quest Challenge (2) LEVEL 3',
        'The Valley -- Valley Zip Line (1) LEVEL 3',
        'The Valley -- Climbing Wall (6) LEVEL 4',
        'The Valley -- Pine Climb (3) LEVEL 5',
        'Boathouse -- Dance Party (15) LEVEL 6',
        'Waterfront -- Shallow Swim (2) Level 5',
        'Waterfront -- Water Park (2)LEVEL 5',
        'Waterfront -- Boating (1) LEVEL 5',
        'White Tent -- Mountain House (12) LEVEL 7',
        'White Tent -- Road House (8) LEVEL 7',
        'White Tent -- White Tent (20) LEVEL 7',
        'The Plateau -- Archery (2) LEVEL 4',
        'The Plateau -- Air Archery (1) LEVEL 3',
        'The Plateau -- Geocaching (2) LEVEL 3',
        'The Plateau -- Orienteering (2) LEVEL 3',
        'Waterside Tent -- Bouncy Boxing (1) LEVEL 3',
        'Waterside Tent -- Gladiator Joust (1) LEVEL 3',
        'Waterside Tent -- Monkey Jumper (4) LEVEL 4',
        'Waterside Tent -- Sticky Dodgeball (1) LEVEL 3',
        'Waterside Tent -- Kickball / Wiffleball (1) LEVEL 2',
        'Waterside Village -- Triple Zip Line (3) LEVEL 5',
        'Waterside Village -- Giant Swings (3) LEVEL 5',
        'Adventure Base Camp -- Geronimo (1) LEVEL 5',
        'Adventure Base Camp -- ABC Zip Line (1) LEVEL 5',
        'Adventure Base Camp -- Water Fall Zip Line (1) LEVEL 5',
        'Adventure Base Camp -- Aerial Park (4) LEVEL 5',
        'Adventure Base Camp -- Parachute Drop (1) LEVEL 5',
        'Adventure Woods -- Adventure Woods (9) LEVEL 4'
    ]

    def generate_activites(self, activities):
        ret_ids = []
        for s in activities:
            z = s[:s.index('--')-1]
            a = s[s.index('--')+3: s.index('(')-1]
            c = int(s[s.index('(')+1:s.index(')')])
            l = int(s[s.index('LEVEL')+6:])
            zone=Zone.objects.get(name=z)
            activity = Activity(
                zone=zone,
                name=a,
                capacity=c,
                level=l
            )
            activity.save()
            ret_ids.append(activity.id)
        return ret_ids

    def generate_periods(self, periods, period_length, first_period):
        ret_ids = []
        hrs = int(first_period[:first_period.index(':')])
        mins = int(first_period[first_period.index(':')+1:])
        date = datetime.datetime(2000,1,1,hrs,mins,0)
        for i in range(periods):
            time = (date+datetime.timedelta(minutes=(i*period_length))).time()
            period = Period(start=time)
            period.save()
            ret_id.append(period.id)
        return ret_id

    def generate_group_leaders(self, amount):
        ret_ids = []
        group = Group.objects.filter(name='GroupLeaders')[0]
        for i in range(amount):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            done = False
            attempt = 1
            while not done:
                try:
                    username = (first_name+last_name+str(attempt)).lower()
                    password = (first_name[0]+last_name[0]+'password')
                    user = User.objects.create_user(username,
                        password=password,
                        first_name=first_name,
                        last_name=last_name
                    )
                    user.save()
                    user.groups.add(group)
                    ret_ids.append(user.id)
                    done = True
                    print 'Created User Cridentials => '+username+':'+password
                except IntegrityError as e:
                    attempt += 1
        return ret_ids

    def generate_programs(self, total_programs, day):
        ret_ids = []
        teams = numpy.random.choice(self.team_names, total_programs)
        group_sizes = [101,26,82,52,40,33]
        for team_name in teams:
            program = Program(
                program_type='YP',
                name=team_name,
                campers=numpy.random.choice(group_sizes,1)[0],
                day=day,
                arrival_time=Period.objects.all()[0],
                departure_time=Period.objects.all()[9]
            )
            program.save()
            ret_ids.append(program.id)
        return ret_ids
