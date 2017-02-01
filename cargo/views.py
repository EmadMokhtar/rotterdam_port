from django.views import generic

from .models import Dock


class DockListView(generic.ListView):
    model = Dock
    queryset = Dock.objects.all().select_related()
    allow_empty = True
    context_object_name = 'docks'


class DockDetailsView(generic.DetailView):
    model = Dock
    context_object_name = 'dock'
    pk_url_kwarg = 'dock_number'
    queryset = Dock.objects.select_related()

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        dock_number = self.kwargs.get(self.pk_url_kwarg)
        return queryset.get(dock_number=dock_number)
