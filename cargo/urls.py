from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^docks/$',
        view=views.DockListView.as_view(),
        name='dock-list'),
    url(r'^docks/(?P<dock_number>[a-zA-Z0-9-]+)/$',
        view=views.DockDetailsView.as_view(),
        name='dock-details'),
]
