from django.contrib import admin

from .models import Container, Dock, DockLog, Ship


class DockAdmin(admin.ModelAdmin):
    list_display = ('dock_number', 'ship_in')


class ContainerAdmin(admin.ModelAdmin):
    list_display = ('ship', 'has_fire', 'has_chemical')


class ShipAdmin(admin.ModelAdmin):
    list_display = ('ship_number', 'dock')


class DockLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'ship', 'action', 'dock')


admin.site.register(Container, ContainerAdmin)
admin.site.register(Dock, DockAdmin)
admin.site.register(Ship, ShipAdmin)
admin.site.register(DockLog, DockLogAdmin)
