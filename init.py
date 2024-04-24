from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from core.models import *
import random

from faker import Faker
fake = Faker()

Organization = apps.get_model('core.organization')

organization, created = Organization.objects.get_or_create(subdomain_prefix='localhost', name='Trans-Academia')
if created: print("Organization created successfully!")

"""
# Menu
employees = [
    'employee.status',
    'employee.agreement',
    'employee.branch',
    'employee.direction',
    'employee.subdirection',
    'employee.service',
    'employee.position',
    'employee.grade',
    'employee.employee',
]

Menu = apps.get_model('core.menu')
Organization = apps.get_model('core.organization')

organization, created = Organization.objects.get_or_create(subdomain_prefix='localhost', name='Trans-Academia')
if created: print("Organization created successfully!")

obj, created = Menu.objects.get_or_create(name='employees', icon='fa fa-users', organization=organization)
if created:
    qs = ContentType.objects.filter(app_label='employee', model__in=[employee.split('.')[-1] for employee in employees])
    obj.children.add(*qs)
    obj.save()
    print("Menu created successfully!")

# initial data
Status = apps.get_model('employee.status')
Agreement = apps.get_model('employee.agreement')
Branch = apps.get_model('employee.branch')
Direction = apps.get_model('employee.direction')
Subdirection = apps.get_model('employee.subdirection')
Service = apps.get_model('employee.service')
Designation = apps.get_model('employee.designation')
Grade = apps.get_model('employee.grade')
Employee = apps.get_model('employee.employee')

status, created = Status.objects.get_or_create(name='en activite', organization=organization)
if created: print("Status created successfully!")

agreement, created = Agreement.objects.get_or_create(name='cdi', organization=organization)
if created: print("Agreement created successfully!")

branch, created = Branch.objects.get_or_create(name='kinshasa', organization=organization)
if created: print("Branch created successfully!")

direction, created = Direction.objects.get_or_create(name='ressource humaine', organization=organization)
if created: print("Direction created successfully!")

subdirection, created = Subdirection.objects.get_or_create(direction=direction, name='personnel', organization=organization)
if created: print("Subdirection created successfully!")

service, created = Service.objects.get_or_create(sub_direction=subdirection,name='paie', organization=organization)
if created: print("Service created successfully!")

designation, created = Designation.objects.get_or_create(name='chef de service', organization=organization)
if created: print("Position created successfully!")

grade, created = Grade.objects.get_or_create(name='A1', organization=organization)
if created: print("Grade created successfully!")

if Employee.objects.count() == 0:
    # create multiple employees
    employees = [
        {
            'registration_number': fake.random_int(min=1000, max=9999),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'middle_name': fake.first_name(),
            'gender': random.choice(['Male', 'Female']),
            'marital_status': random.choice(['Maried', 'Single', 'Widower']),
            'email': fake.email(),
            'mobile_number': fake.phone_number(),
            'status': status,
            'agreement': agreement,
            'branch': branch,
            'direction': direction,
            'sub_direction': subdirection,
            'service': service,
            'designation': designation,
            'grade': grade,
            'date_of_birth': fake.date_of_birth(),
            'date_of_join': fake.date_of_birth().replace(year=random.randint(2022, 2024)),
            'physical_address': fake.address(),
            'organization': organization,
            'payment_method': random.choice(['Cash', 'Bank', 'Mobile Money']),
        }
        for i in range(50)
    ]

    # Bulk create employees
    Employee.objects.bulk_create([Employee(**employee) for employee in employees])
    print("Employees created successfully!")

# Leave
leaves = [
    'leave.typeofleave',
    'leave.holiday',
    'leave.earlyleave',
    'leave.leave',
]

obj, created = Menu.objects.get_or_create(name='congés', icon='fa fa-calendar', organization=organization)
if created:
    qs = ContentType.objects.filter(app_label='leave', model__in=[leave.split('.')[-1] for leave in leaves])
    obj.children.add(*qs)
    obj.save()
    print("Menu created successfully!")

TypeOfLeave = apps.get_model('leave.typeofleave')
Holiday = apps.get_model('leave.holiday')

type_of_leave, created = TypeOfLeave.objects.get_or_create(name='congé annuel', max_days_per_year=30, organization=organization)
if created: print("TypeOfLeave created successfully!")

holiday, created = Holiday.objects.get_or_create(name='noel', start_dt=fake.date_this_year(before_today=True), end_dt=fake.date_this_year(after_today=True), organization=organization)
if created: print("Holiday created successfully!")
"""

payrolls = [
    'payroll.payroll',
    'payroll.payslip',
    'payroll.item',
]

obj, created = Menu.objects.get_or_create(name='payroll', icon='fa fa-cash', organization=organization)
if created:
    qs = ContentType.objects.filter(app_label='payroll', model__in=[payroll.split('.')[-1] for payroll in payrolls])
    obj.children.add(*qs)
    obj.save()
    print("Menu created successfully!")

Item = apps.get_model('payroll.item')

items = [{
    'code': 'SAL',
    'name': 'Salaire de base',
    'formula': '100000',
    'condition': '1',
    'is_taxable': True,
    'is_social_security': True,
    'organization': organization,
}, {
    'code': 'PRIM-1',
    'name': 'Prime de rendement',
    'formula': '400000',
    'condition': '1',
    'is_taxable': True,
    'is_social_security': True,
    'organization': organization,
}, {
    'code': 'VC',
    'name': 'Vie Cher',
    'formula': '200000',
    'condition': '1',
    'is_taxable': False,
    'is_social_security': True,
    'organization': organization,
}]

items = [Item(**item) for item in items]

if Item.objects.count() == 0:
    Item.objects.bulk_create(items)
    print("Items created successfully!")