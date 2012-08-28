from django.conf.urls import patterns, include, url
from tailor.servent.views import fab

urlpatterns = patterns('',    
    url(r'^api/v1/fab/(?P<object_id>\d+)$', fab, name='fab'),
)

