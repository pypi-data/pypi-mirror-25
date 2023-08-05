import subprocess
from django.core import management
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'CI/CD'

    def handle(self, *args, **options):
        pass

