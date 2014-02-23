from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Shortcut to run the dev server on 0.0.0.0:8000"

    def handle(self, *args, **options):
        call_command('runserver',  '0.0.0.0:8000')