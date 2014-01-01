from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib.auth.views import login as login_view, logout as logout_view

from .views import *

urlpatterns = patterns('',
    url(r'^$', index_view, name="index", ),
    url(r'^add/$', add_view, name="add", ),
    url(r'^paste/(?P<paste_pk>[-\w\d]+)/$', detail_view, name="detail", ),
    url(r'^paste/raw/(?P<paste_pk>[-\w\d]+)/$', raw_view, name="raw", ),
    url(r'^paste/(?P<paste_pk>[-\w\d]+)/edit/$', edit_view, name="edit", ),
    url(r'^paste/(?P<paste_pk>[-\w\d]+)/delete/$', delete_view, name="delete", ),
    url(r'^paste/(?P<paste_pk>[-\w\d]+)/delete-process/$', delete_process, name="delete_process", ),

    url(r'^login/$', login_view, name="login", ),
    url(r'^logout/$', logout_view, name="logout", ),
)