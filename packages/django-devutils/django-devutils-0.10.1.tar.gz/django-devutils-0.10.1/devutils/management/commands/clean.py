import os
from django.core import management
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Clean'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            default=False,
            help='Delete all migrations',
        )

    def write(self, text):
        return self.stdout.write(self.style.SUCCESS(text))

    def handle(self, *args, **options):
        if options['all']:
            self.write('Remove migrations')
            management.call_command('cleanmigrations')

        self.write('Removing database')
        os.remove(settings.DATABASES['default']['NAME'])

        self.write('Create migrations')
        management.call_command('makemigrations')

        self.write('Migrate database')
        management.call_command('migrate')

        self.write('Load fixtures')
        for filename in os.listdir('fixtures'):
            management.call_command('loaddata', f'fixtures/{filename}', verbosity=2, ignorenonexistent=True)
