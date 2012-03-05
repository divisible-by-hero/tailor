from fabric.api import execute
from django.http import HttpResponse



def kick_apache():
    """ Kick the apache server for this app. """
    hello = run('sudo %s graceful' % env.apache_bin_dir)
    return hello
    
def break_apache():
    run('%s graceful' % env.apache_bin_dir)