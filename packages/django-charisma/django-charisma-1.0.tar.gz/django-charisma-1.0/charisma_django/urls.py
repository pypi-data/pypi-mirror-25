from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index.html'),
    url(r'^index.html$', views.index, name='index.html'),
    url(r'^ui.html$', views.ui, name='ui.html'),
    url(r'^form.html$', views.form, name='form.html'),
    url(r'^chart.html$', views.chart, name='chart.html'),
    url(r'^typography.html$', views.typography, name='typography.html'),
    url(r'^gallery.html$', views.gallery, name='gallery.html'),
    url(r'^tables.html$', views.tables, name='tables.html'),
    url(r'^calendar.html$', views.calendar, name='calendar.html'),
    url(r'^grid.html$', views.grid, name='grid.html'),
    url(r'^tour.html$', views.tour, name='tour.html'),
    url(r'^icons.html$', views.icons, name='icons.html'),
    url(r'^error.html$', views.error, name='error.html'),
    url(r'^login.html$', auth_views.LoginView.as_view(template_name='charisma_django/pages/login.html',
                                                      redirect_field_name='/login.html')),
    url(r'^logout.html$', auth_views.LogoutView.as_view(template_name='charisma_django/pages/login.html',
                                                        redirect_field_name='/login.html'))
]
