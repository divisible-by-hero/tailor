from __future__ import with_statement
from fabric.api import *

from tailor.decorators import tailored, dependency

env.PROJECT_ID = PROJECT_ID
env.PROJECT_USER = PROJECT_USER

env.id = env.PROJECT_ID
env.user = PROJECT_USER
env.project_virtual = '/srv/www/.virtualenvs/%s' % env.PROJECT_ID
env.activate = 'source /srv/www/.virtualenvs/%s/bin/activate' % env.PROJECT_ID
env.apache_bin_dir = "/etc/init.d/apache2"
env.log_location = "/var/log/apache2/error.log"


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
        

@dependency
def test_dependent(number):
    number = number * 3
    return "%s scoops"

@tailored
def test_task(number, flavor, mascot='Willie the Wildcat'):
    scoops = test_dependent(number)
    print "I could eat %s of %s ice cream!." % (scoops, flavor)
    print "The best college mascot is  %s!" % mascot



