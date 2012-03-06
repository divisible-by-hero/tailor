#Tailor
Tailor is a Django app that let's you run Fabric commands via a web based API.

###Running Tailor on a seperate host
Optimally, Tailor should be installed on different host than the target host.  In other words, a project running Tailor on Host1 will execute Fabric commands on Host2.

###Running Tailor on the same host
Tailor can also run on the same host you want to run Fabric commands on.  However, caution must be exercised or Tailor could cause some funky behavior. For example, if a Fabric command deleted the very project running Tailor.

##Getting started
###Install 'tailor' in a Django Project
pip install 'tailor'
Add 'tailor' to 'installed_apps' in your Django settings file include 'tailor.urls' in your urls conf.

Add TAILOR_API_KEYS, a list of accepted keys, to your Django settings file.

###Install 'tailor.client' in a remote host
pip install 'tailor'
In your fabfile,
'from tailor.client import tailored'
To make Fabric commands available to Tailor, add the @tailored decorator to any Fabric function.

##API
###Returns a list of the available Fabric commands, including docstrings and required parameters
/tailor/api/schema/?host=example.com&pathtofabfile=/srv/www/projects/exampleproject/fabfile.py&apikey=XXXXXXXXX
Method: GET

###Run Fabric commands
/tailor/api/fab/
Method: POST

POST DATA (for a remote host)::

    {
        'hosts': [
            'http://server1.example.com',
            'http://server2.example.com',
            'http://server3.example.com'
        ],
        'virtualenv': 'sampleproject',
        'fabfile_path': '/srv/www/projects/exampleproject/fabfile.py',
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
        'apikey': 'XXXXXXXXX'
    }

POST DATA (for the same host)::

    {
        'hosts': 'self',
        'commands': [
            {'command': 'production'},
            {'command': 'restart_apache'}
        ]
    }

#Docs
Check out the full documentation.

http://readthedocs.org/docs/tailor/en/latest/