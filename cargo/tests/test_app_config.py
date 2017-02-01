from django.apps import apps
from django.test import TestCase


class TestCargoWebConfig(TestCase):
    def setUp(self):
        self.app = apps.get_app_config('cargo')

    def test_app_name(self):
        self.assertEqual('cargo', self.app.name)

    def test_app_verbose_name(self):
        self.assertEqual('Rotterdam Port Cargo App', self.app.verbose_name)
