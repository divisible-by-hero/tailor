import pickle
import inspect
import simplejson
import urllib2

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from fabric.api import *

def tailored(request):
    '''
    Parses the project fabfile and returns API listing
    the available commands.  Commands are made available by
    adding the @tailored (name?) decorator to a fabric function.
    '''
    
    #The directory that hold the fabfile needs to be added to the python path
    from conf import fabfile
    
    fab_props = dir(fabfile)
    
    # Exclude certain properties in the fabfile
    # TODO: replace by opting in with decorator, instead of opting everything else out
    exclude_list = ['__builtins__', '__doc__', '__file__', '__name__', '__package__', 'abort', 'cd', 'execute', 'fastprint', 'get', 'glob', 'hide', 'hosts',  'lcd',  'local',  'open_shell', 'os', 'output', 'parallel', 'path',  'prefix', 'prompt', 'put', 'puts', 'reboot',  'requests', 'require', 'roles', 'run', 'runs_once', 'serial', 'settings', 'setup', 'show', 'simplejson', 'ssh', 'sudo', 'task', 'time', 'warn', 'with_settings', 'with_statement']
 

    fab_dict = {}
    for prop in fab_props:
        if not prop in exclude_list: # TODO: Only add to fab_dict opted in tasks
            # If it's a callable, pickle it
            if hasattr( eval('fabfile.%s' % prop), '__call__' ):
                _callable = eval('fabfile.%s' % prop)
                callable_source = inspect.getsource(_callable)
                fab_dict[prop] = pickle.dumps(callable_source)
            # Else just use the value
            else:
                fab_dict[prop] = eval('fabfile.%s' % prop)
    
    #response = {}
    response = simplejson.dumps(fab_dict)    
    
    return HttpResponse(response, mimetype='application/json', status=200)
    
def fab(request):
    '''
    Accepts JSON (and more later on?) data describing fabric commands
    and runs them if they exist and are allowed.
    '''

    # NOTE: This is all PoC at this point.  Lots of hard-coded values    

    try:
        client_url = "http://localhost:8001/tailor/api/v1/tailored/"
        client_data = urllib2.urlopen(client_url)
        client_json = client_data.read()
        client_dict = simplejson.loads(client_json)
    
        #Need this?
        from fabric.api import env
    
        # TODO: dynamically configure the 'env' dict from
        #env = client_dict['env']
    
        # TODO: removing these hard coded values.  either use 'env' values from client api or POST data
        env.apache_bin_dir = "/etc/init.d/apache2"
        env.hosts = ['host_name_removed']
        env.user = 'fabric'
    
        # TODO: Get these function strings from the client api instead of hard-coded
        picklefunction = "S'def kick_apache():\\n \"\"\" Kick the apache server for this app. \"\"\"\\n run(\\'sudo %s graceful\\' % env.apache_bin_dir)\\n'\np0\n."
        stringfunction = pickle.loads(str(picklefunction))
    
        # TODO: Do this dynamically
        function_dictionary = {}
        exec stringfunction in globals(), function_dictionary
        kick_apache = function_dictionary['kick_apache']

        # TODO: Call the fabric tasks listed in the POST data
        execute(kick_apache)
    
        #respond
        response_dict = {'success':True, 'message':"Commands Executed"}
        response = simplejson.dumps(response_dict)
        return HttpResponse(response, mimetype='application/json', status=200)
    except:
        response_dict = {'success':False, 'message':"Coudn't not execute commands"}
        response = simplejson.dumps(response_dict)
        return HttpResponse(response, mimetype='application/json', status=400)
    
