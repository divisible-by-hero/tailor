from django.conf.urls import patterns, include, url
from tailor.servent.views import fab, projects

urlpatterns = patterns('',    
    url(r'^api/v1/fab/(?P<object_id>\d+)$', fab, name='fab'),
    url(r'^api/v1/projects/(?P<object_id>\d+)$', projects, name='project'),
    url(r'^api/v1/projects/$', projects, name='projects'),
)

