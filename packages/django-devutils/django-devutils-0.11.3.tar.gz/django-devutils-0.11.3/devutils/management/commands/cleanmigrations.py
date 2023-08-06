import os
import glob
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Remove migrations files'

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, '**', 'migrations', '*.py')
        files = [filename for filename in glob.glob(path, recursive=True) if not filename.endswith('__init__.py')]

        for file in files:
            self.stdout.write(f'Removing file: {file}')
            os.remove(file)
