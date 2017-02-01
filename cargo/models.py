# from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class Ship(models.Model):
    ship_number = models.CharField(max_length=15,
                                   verbose_name=_('ship number'), unique=True)
    # captain = models.OneToOneField(to=User, on_delete=models.CASCADE,
    #                                null=True, blank=True)

    def has_fire_hazard(self):
        """Flag whether ship has containers with fire hazard"""
        return self.containers.filter(ship=self, has_fire=True).count() > 0

    def has_chemical_hazard(self):
        """Flag whether ship has containers with chemical hazard"""
        return self.containers.filter(ship=self, has_chemical=True).count() > 0

    def __str__(self):
        return self.ship_number


class Container(models.Model):
    ship = models.ForeignKey(to=Ship, related_name='containers')
    has_fire = models.BooleanField(
        verbose_name=_('fire hazard'), default=False)
    has_chemical = models.BooleanField(verbose_name=_('chemical hazard'),
                                       default=False)

    def __str__(self):
        return "Container No. {}".format(self.pk)


class Dock(models.Model):
    dock_number = models.CharField(max_length=15,
                                   verbose_name=_('dock number'), unique=True)
    ship_in = models.OneToOneField(to=Ship, related_name='dock',
                                   null=True, blank=True)

    def get_absulote_url(self):
        from django.urls import reverse
        kwargs = {
            'dock_number': self.dock_number,
        }
        return reverse('dock-details', kwargs=kwargs)

    def __str__(self):
        return self.dock_number

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.pk is not None:  # Update
            orignal = Dock.objects.get(pk=self.pk)
            # Ship entering to dock
            if self.ship_in is not None and orignal.ship_in is None:
                log = self.create_in_log(self.ship_in)
                log.save()
            # Ship exting from dock
            elif self.ship_in is None and orignal.ship_in is not None:
                log = self.create_out_log(orignal.ship_in)
                log.save()
            # User assign different ship for occuipied dock
            elif self.ship_in is not None:
                if self.ship_in != orignal.ship_in:
                    raise ValidationError('Dock is already occupied')
        return super(Dock, self).save(*args, **kwargs)

    def logs(self):
        return self.dock_logs.all()

    def _create_log(self, ship, action):
        return DockLog(ship=ship, dock=self, action=action)

    def create_in_log(self, ship):
        return self._create_log(ship=ship,
                                action=IN_ACTION)

    def create_out_log(self, ship):
        return self._create_log(ship=ship,
                                action=OUT_ACTION)

IN_ACTION = 'in'
OUT_ACTION = 'out'
LOG_ACTIONS_CHOICES = (
    (IN_ACTION, _('In')),
    (OUT_ACTION, _('Out')),
)


class DockLog(models.Model):
    dock = models.ForeignKey(to=Dock, related_name='dock_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=5, choices=LOG_ACTIONS_CHOICES)
    ship = models.ForeignKey(to=Ship, related_name='ship_logs')

    class Meta:
        ordering = ['-timestamp']
