from django.conf import settings
from django.core.management.base import BaseCommand

PROJECT_NAME = settings.WSGI_APPLICATION.split('.')[0]
SKIP = []

HEADER = f"""[main]
host = https://www.transifex.com

[{PROJECT_NAME}.main]
file_filter = {PROJECT_NAME}/locale/<lang>/LC_MESSAGES/django.po
source_file = {PROJECT_NAME}/locale/en/LC_MESSAGES/django.po
source_lang = en
type = PO
"""

TEMPLATE = """
[{project}.{name}]
file_filter = {path}/locale/<lang>/LC_MESSAGES/django.po
source_file = {path}/locale/en/LC_MESSAGES/django.po
source_lang = en
type = PO
"""


class Command(BaseCommand):
    help = 'Generates transifex config'

    def handle(self, *args, **options):
        self.stdout.write(HEADER)

        for app in settings.INSTALLED_APPS:
            if app.startswith(PROJECT_NAME) and app not in SKIP:
                path = app.replace('.', '/')
                project = PROJECT_NAME
                name = app.split('.')[-1]
                self.stdout.write(TEMPLATE.format(**locals()))
