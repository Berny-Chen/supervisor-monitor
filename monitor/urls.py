from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^xmlrpc/$', views.xmlrpc, name='xmlrpc'),
    url(r'^config/$', views.config, name='config'),
    url(r'^config/admin/$', views.config_admin, name='config_admin'),
    url(r'^config/sync/$', views.config_sync, name='config_sync'),
    url(r'^config/reload/$', views.config_reload, name='config_reload'),
]
