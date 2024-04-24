from django.core.management.base import BaseCommand
from core.models import Organization


class Command(BaseCommand):
    help = "Create organization"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Organization name: ")

    def handle(self, *args, **options):
        obj, created = Organization.objects.get_or_create(name=options["name"])
        message = "Organization created" if created else "Organization already exists"
        self.stdout.write(self.style.SUCCESS(message))

            