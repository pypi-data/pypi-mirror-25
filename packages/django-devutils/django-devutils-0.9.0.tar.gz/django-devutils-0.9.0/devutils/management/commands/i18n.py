from django.conf import settings
from django.core.management.base import BaseCommand


PROJECT_NAME = settings.WSGI_APPLICATION.split('.')[0]
SKIP = []


class Command(BaseCommand):
    help = 'Makemessages for each app in settings.INSTALLED_APPS'

    def handle(self, *args, **options):
        self.stdout.write('Generating localized messages')

        for app in settings.INSTALLED_APPS:
            if app.startswith(PROJECT_NAME) and app not in SKIP:
                path = app.replace('.', '/')
                self.stdout.write(path)
