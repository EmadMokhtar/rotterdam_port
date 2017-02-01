from django.core.exceptions import ValidationError
from django.test import TestCase

from cargo.models import IN_ACTION, OUT_ACTION, Container, Dock, DockLog, Ship


class DockTestCases(TestCase):

    def setUp(self):
        self.dock = Dock.objects.create(dock_number='DC-01')
        self.ship = Ship.objects.create(ship_number='SH-01')

    def test_dock_log_ship_enter(self):
        # Ship Enter to Dock
        self.dock.ship_in = self.ship
        self.dock.save()
        logs = self.dock.logs()
        self.assertEqual(1, len(logs))
        self.assertEqual(IN_ACTION, logs[0].action)

    def test_dock_log_ship_exit(self):
        # Ship Enter to Dock
        self.dock.ship_in = self.ship
        self.dock.save()
        # Ship Exit from Dock
        self.dock.ship_in = None
        self.dock.save()
        logs = self.dock.logs()
        self.assertEqual(2, len(logs))
        self.assertEqual(OUT_ACTION, logs[0].action)
        self.assertEqual(IN_ACTION, logs[1].action)

    def test_create_in_log(self):
        log = self.dock.create_in_log(self.ship)
        self.assertIsInstance(log, DockLog)
        self.assertEqual(IN_ACTION, log.action)
        self.assertEqual(self.ship.pk, log.ship_id)

    def test_create_out_log(self):
        log = self.dock.create_out_log(self.ship)
        self.assertIsInstance(log, DockLog)
        self.assertEqual(OUT_ACTION, log.action)
        self.assertEqual(self.ship.pk, log.ship_id)

    def test_str(self):
        self.assertEqual('DC-01', self.dock.__str__())
        self.assertEqual('DC-01', str(self.dock))

    def test_update_dock_wont_create_dublicate_log(self):
        self.dock.ship_in = self.ship
        self.dock.save()
        self.dock.save()
        self.assertEqual(1, len(self.dock.logs()))

    def test_assign_ship_for_occupied(self):
        self.dock.ship_in = self.ship
        self.dock.save()
        ship = Ship.objects.create(ship_number='SH-02')
        self.dock.ship_in = ship
        with self.assertRaisesMessage(ValidationError,
                                      'Dock is already occupied'):
            self.dock.save()

    def test_dock_absulote_url(self):
        self.assertEqual('/cargo/docks/DC-01/', self.dock.get_absulote_url())


class ShipTestCases(TestCase):

    def setUp(self):
        self.ship = Ship.objects.create(ship_number='SH-01')

    def test_str(self):
        self.assertEqual('SH-01', self.ship.__str__())
        self.assertEqual('SH-01', str(self.ship))

    def test_with_container_has_fire_hazard(self):
        Container.objects.create(ship=self.ship, has_fire=True)
        self.assertTrue(self.ship.has_fire_hazard())

    def test_with_container_has_not_fire_hazard(self):
        Container.objects.create(ship=self.ship, has_fire=False)
        self.assertFalse(self.ship.has_fire_hazard())

    def test_with_container_has_chemical_hazard(self):
        Container.objects.create(ship=self.ship, has_chemical=True)
        self.assertTrue(self.ship.has_chemical_hazard())

    def test_with_container_has_not_chemical_hazard(self):
        Container.objects.create(ship=self.ship, has_chemical=False)
        self.assertFalse(self.ship.has_chemical_hazard())


class ContainerTestCase(TestCase):

    def setUp(self):
        ship, created = Ship.objects.get_or_create(ship_number='SH-01')
        self.containter, created = Container.objects.get_or_create(ship=ship)

    def test_str(self):
        self.assertEqual('Container No. 1', self.containter.__str__())
        self.assertEqual('Container No. 1', str(self.containter))
