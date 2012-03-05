from django.conf.urls.defaults import patterns, include, url
from tailor.views import *

urlpatterns = patterns('',
    url(r'^$', stats),
    url(r'^home/$', home),
    url(r'^command/(?P<command>[-\w]+)/$', command),

    url(r'^api/schema/$', schema, name='schema'),
    url(r'^api/$', endpoint, name='endpoint'),

)

