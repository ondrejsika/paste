from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView

from .views import *

urlpatterns = patterns('',
    url(r'^$', index_view, name="index", ),
    url(r'^add/$', add_view, name="add", ),
    url(r'^paste/(?P<paste_pk>[-\w\d]+)/$', detail_view, name="detail", ),
)