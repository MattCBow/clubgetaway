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


    def create_program(self, program_type_name, program_name, start_date, end_date, guest_names):
        program_type = ProgramType.objects.filter(name=program_type_name)[0]
        program = Program(
            name='here',
            program_type=program_type,
            start_date=start_date,
            end_date=end_date
        )
        program.save()
        num_of_groups = (program_type.group_capacity/len(guest_names))+1
        for group_id in range(num_of_groups):
            group = Group(
                program=program,
                number=group_id
            )
            group.save()
            for name in guest_names[group_id::num_of_groups]:
                guest = Guest(
                    group=group,
                    first_name=name['first'],
                    last_name=name['last']
                )
                guest.save()

    def generate_program(self, program_type_name, program_name, start_date, end_date, number_of_guests):
        return self.create_program(
            program_type_name=program_type_name,
            program_name=program_name,
            start_date=start_date,
            end_date=end_date,
            guest_names=self.generate_names(number_of_guests)
        )

'''
from scheduler.generator import *
test = UserTester()
test.generate_program(
    program_type_name='Youth Program',
    program_name='First Program',
    start_date='2017-01-01',
    end_date='2017-01-02',
    number_of_guests=100
)
'''
