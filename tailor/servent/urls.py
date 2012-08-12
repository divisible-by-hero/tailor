from django.conf.urls.defaults import patterns, include, url
from tailor.servent.views import *

urlpatterns = patterns('',    
    url(r'^api/v1/fab/$', fab, name='fab'),
)

