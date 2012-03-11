import pickle
import inspect
import simplejson

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
