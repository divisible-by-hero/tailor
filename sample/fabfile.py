from __future__ import with_statement
from fabric.api import *

from tailor.client.decorators import tailored, dependency

"""
If you import values, remember to store them in the 'env' dictionary
so tailor has access to them.
"""
from project import PROJECT_ID, PROJECT_USER
env.id = PROJECT_ID
env.user = PROJECT_USER

env.project_virtual = '/srv/www/.virtualenvs/%s' % env.PROJECT_ID
env.activate = 'source /srv/www/.virtualenvs/%s/bin/activate' % env.PROJECT_ID
env.apache_bin_dir = "/etc/init.d/apache2"
env.log_location = "/var/log/apache2/error.log"



"""
Internally used object need the @dependency decorator so that other 
tasks can use them.
"""
@dependency
def test_dependent(number):
    number = number * 3
    return "%s scoops"

"""
Add the @tailored decorator to expose a task to the Tailor API. Remember to
include docstrings with every task to provide documentation to users.
"""
@tailored
def test_task(number, flavor, mascot='Willie the Wildcat'):
    """ An example task that prints out a few favorites. """
    scoops = test_dependent(number)
    print "I could eat %s of %s ice cream!." % (scoops, flavor)
    print "The best college mascot is  %s!" % mascot
    




@dependency    
def virtualenv(command):
    with cd(env.directory):
        run(env.activate + '&&' + command)

@tailored
def view_log():
    """ View the log file """
    run('sudo cat %s' % env.log_location)

@tailored
def kick_apache():
    """ Kick the apache server. """
    run('sudo %s graceful' % env.apache_bin_dir)

@tailored
def alpha():
    """ Set environment to alpha. """
    env.branch = "alpha"
    env.hosts = ["alpha1.example.com", "alpha2.example.com"]

@tailored
def production():
    """ Set environment to production. """
    env.branch = "production"
    env.hosts = ["prod1.example.com", "prod2.example.com"]

@tailored
def deploy(release_tag=None):
    """ Deploy an app on either alpha or production.  If production, a tag is required. """
    if env.branch == "production" and release_tag:
        print "...deploying release: %s" % release_tag
        kick_apache()        
    elif env.branch == "alpha":
        print "...deploying master alpha branch..."
        kick_apache()
    else:
        print "Did not deploy"
        
