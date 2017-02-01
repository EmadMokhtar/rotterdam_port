from django.test import TestCase
from django.urls import reverse

from cargo.models import Dock


class DockListViewTestCases(TestCase):

    def test_view_url(self):
        self.assertEqual(reverse('dock-list'), '/cargo/docks/')

    def test_empty_dock_list(self):
        response = self.client.get(reverse('dock-list'))
        print(response.status_code)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.context['docks']))

    def test_dock_list(self):
        for i in range(10):
            Dock.objects.create(dock_number='DC-{}'.format(i))
        response = self.client.get(reverse('dock-list'))
        print(response.status_code)
        self.assertEqual(200, response.status_code)
        self.assertEqual(10, len(response.context['docks']))


class DockDetailViewTestCases(TestCase):

    def setUp(self):
        self.dock = Dock.objects.create(dock_number='DC-01')

    def test_view_url(self):
        self.assertEqual(reverse('dock-details',
                                 kwargs={'dock_number': self.dock.dock_number}),
                         '/cargo/docks/DC-01/')

    def test_dock_details(self):
        response = self.client.get(reverse('dock-details',
                                           kwargs={'dock_number': self.dock.dock_number}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.dock, response.context['dock'])
