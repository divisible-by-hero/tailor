from django.conf.urls.defaults import patterns, include, url
from tailor.views import *

urlpatterns = patterns('',    
    url(r'^api/v1/schema/$', schema, name='schema'),
    url(r'^api/v1/fab/$', fab, name='fab'),

)

