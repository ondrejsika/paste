from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib.auth.views import login as login_view, logout as logout_view

from .views import *

urlpatterns = patterns('',
    url(r'^$', index_view, name="index", ),
    url(r'^my/$', index_my_view, name="index_my", ),
    url(r'^add/$', add_view, name="add", ),
    url(r'^paste/(?P<paste_pk>[-\w\d]+)/$', detail_view, name="detail", ),
    url(r'^paste/raw/(?P<paste_pk>[-\w\d]+)/$', raw_view, name="raw", ),
    url(r'^paste/(?P<paste_pk>[-\w\d]+)/edit/$', edit_view, name="edit", ),
    url(r'^paste/(?P<paste_pk>[-\w\d]+)/delete/$', delete_view, name="delete", ),
    url(r'^paste/(?P<paste_pk>[-\w\d]+)/delete-process/$', delete_process, name="delete_process", ),

    url(r'^settings/$', settings_view, name="settings", ),
    url(r'^change-password/$', change_password_view, name="change_password", ),
    url(r'^change-password/done/$', TemplateView.as_view(template_name="paste/change_password_done.html"), name="change_password_done", ),

    url(r'^login/$', login_view, name="login", ),
    url(r'^logout/$', logout_view, name="logout", ),
)