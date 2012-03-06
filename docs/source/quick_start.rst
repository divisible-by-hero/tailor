===========
Quick Start
===========


Requirements
============

* Django 1.3.x or greater
* Fabric


Installation
============

To install Tailor simply install via pip::

    pip install tailor
    
Add application to installed apps::

    INSTALLED_APPS = (
        'tailor',
    )
    
Add tailor.urls to your url conf::

    urlpatterns = patterns('',
    
        url(r'^tailor/', include('tailor.urls')),
    )