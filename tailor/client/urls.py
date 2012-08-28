from django.conf.urls import patterns, include, url
from tailor.client.views import schema

urlpatterns = patterns('',    
    url(r'^api/v1/schema/$', schema, name='schema'),
)

