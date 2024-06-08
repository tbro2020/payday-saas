from django.db import transaction
from django.core.management import call_command

with transaction.atomic(using='default'):
    print("Starting...")
    call_command('loaddata', 'db.json', database='default')
    print("Done.")