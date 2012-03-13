===========
Quick Start
===========


Requirements
============

* Django 1.3.x or greater
* Fabric


Installation
============

Client Installation
-------------------

To install Tailor simply install via pip::

    pip install tailor
    
Add application to installed apps::

    INSTALLED_APPS += (
        'tailor',
    )
    
Add tailor.urls to your url conf::

    urlpatterns = patterns('',
    
        url(r'^tailor/', include('tailor.urls')),
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

In your fabfile, ``from tailor.client import tailored``.  To make Fabric commands available to Tailor, add the ``@tailored`` decorator to any Fabric function.
For functions that may be used by fabric tasks, but shouldn't be directly callable via the api, add the ``@dependency`` decorator.

Returns a list of the available Fabric commands, including docstrings and required parameters
``/tailor/api/schema/?key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX``
Method: GET

Server Installation
-------------------

Run Fabric commands
/tailor/api/fab/
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
                    'Fixed issue #31'
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
