from django.conf.urls.defaults import patterns, include, url
from tailor.views import *

urlpatterns = patterns('',    
    url(r'^api/v1/tailored/$', tailored, name='tailored'),
    url(r'^api/v1/fab/$', fab, name='fab'),

)

