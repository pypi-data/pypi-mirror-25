import logging
from django.contrib.auth.models import User
from django.test import TestCase


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime).19s] %(levelname).3s %(message)s')


class Test(TestCase):

    assert_http_status = [
    ]

    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.user = User.objects.create_superuser('testrunner', 'test@test.com', 'testrunner')
        self.client.login(username='testrunner', password='testrunner')

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_url(self):
        errors = []

        for row in self.assert_http_status:

            if row.get('skip'):
                msg = 'skip'
                logging.warning(f'{msg:5}: {url}')
                continue

            url = row['url']
            status = row['status']
            response = self.client.get(url)

            if response.status_code == status:
                msg = 'good'
                self.logger.info(f'{msg:5} {status} {url}')
            else:
                msg = 'error'
                self.logger.error(f'{msg:5} {response.status_code} {url}')
                errors.append(url)

        raise AssertionError(f'HTTP errors {errors}')