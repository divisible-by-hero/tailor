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

Client Installation
-------------------
    
Add application to installed apps::

    INSTALLED_APPS += (
        'tailor.client',
    )
    
Add tailor.urls to your url conf::

    urlpatterns = patterns('',
    
        url(r'^tailor/', include('tailor.client.urls')),
    )
    
Add ``TAILOR_FABFILE_PATH``, a path to your fabfile, to your Django settings file.::

    TAILOR_FABFILE_PATH = "/path/to/your/fabfile.py"

Add ``TAILOR_API_KEYS``, a dictionary of accepted keys, to your Django settings file.::

    TAILOR_API_KEYS = {
        'dashboard':'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        'hubot':'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',
        'arduinio':'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ',
    }

.. note::

    Tailor includes a simple alphanumeric key generator.  ``from tailor import keygen`` then run ``keygen.generate(32)``

In your fabfile, ``from tailor.client.decorators import tailored``.  To make Fabric commands available to Tailor, add the ``@tailored`` decorator to any Fabric function.
For functions that may be used by other fabric tasks, but shouldn't be directly callable via the api, add the ``@dependency`` decorator.

Returns a list of the available Fabric commands, including docstrings and required parameters
``/tailor/api/schema/?key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX``
Method: GET

Servent Installation
--------------------

Add application to installed apps::

    INSTALLED_APPS += (
        'tailor.servent',
    )
    
Add tailor.urls to your url conf::

    urlpatterns = patterns('',
    
        url(r'^tailor/', include('tailor.servent.urls')),
    )

Using the Admin
~~~~~~~~~~~~~~~

If you don't want to make your own custom Tailor client, you can use the admin.
Add entries to the Project model including the location of a tailor schema and a valid Tailor api key.
Execute commands from with the change form page in the admin.

Rolling your own Client
~~~~~~~~~~~~~~~~~~~~~~~

You can make any number of clients with any language, device, or method.
Simply post JSON to a tailor fab location with the following information.

If you project is recorded in the Tailor Project model, you can include the id
in the Tailor fab api.  Otherwise, omit an id and provide a ``schema_url`` and an ``api_key``

Run Fabric commands

URL: /your_tailor_url_path/api/v1/fab/<id>

Method: POST

POST DATA (for a remote host)::

    {
        'hosts': [
            'http://server1.example.com',
            'http://server2.example.com',
            'http://server3.example.com'
        ],
        'commands': [
            {'command': 'alpha'},
            {
                'command': 'deploy',
                'parameters': [
                    '0.96',
                ]
            }
        ],
        'apikey': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    }

POST DATA (for the same host)::

    {
        'hosts': 'self',
        'commands': [
            {'command': 'production'},
            {'command': 'restart_apache'}
        ]
    }
