import pickle
import inspect
import simplejson
import urllib2
import sys

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from fabric.api import *

from tailor.decorators import tailored

def schema(request):
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
    exclude_list = ['__builtins__', '__doc__', '__file__', '__name__', '__package__', 'abort', 'cd', 'execute', 'fastprint', 'get', 'glob', 'hide', 'hosts',  'lcd',  'local',  'open_shell', 'os', 'output', 'parallel', 'path',  'prefix', 'prompt', 'put', 'puts', 'reboot',  'requests', 'require', 'roles', 'run', 'runs_once', 'serial', 'settings', 'setup', 'show', 'simplejson', 'ssh', 'sudo', 'task', 'time', 'warn', 'with_settings', 'with_statement', 'paths',]
 

    fab_dict = {}
    fab_tasks = {}
    fab_dependencies = {}
    fab_dict['tasks'] = fab_tasks
    fab_dict['dependencies'] = fab_dependencies
    
    for prop in fab_props:
        if not prop in exclude_list:
            # If it's a callable, pickle it
            if hasattr( eval('fabfile.%s' % prop), '__call__' ):
                if hasattr( eval('fabfile.%s' % prop), 'tailored' ):
                    _callable = eval('fabfile.%s' % prop)
                    callable_source = inspect.getsource(_callable)
                    fab_tasks[prop] = (pickle.dumps(callable_source))
                elif hasattr( eval('fabfile.%s' % prop), 'dependency' ):
                    _callable = eval('fabfile.%s' % prop)
                    callable_source = inspect.getsource(_callable)
                    fab_dependencies[prop] = (pickle.dumps(callable_source))
            # Else just use the value
            else:
                fab_dict[prop] = eval('fabfile.%s' % prop)
    
    #response = {}
    response = simplejson.dumps(fab_dict)    
    
    return HttpResponse(response, mimetype='application/json', status=200)


@csrf_exempt    
def fab(request):
    '''
    Accepts JSON (and more later on?) data describing fabric commands
    and runs them if they exist and are allowed.

    #Test it locally
    curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"hosts": ["server1.example.com"],"commands": ["alpha", "kick_apache"] }' http://localhost:8000/tailor/api/v1/fab/

    # NOTE: This is all PoC at this point.  Lots of hard-coded values
    # TODO: Seperate all this out to methods
    '''
    
    import fabric

    # Turn off output as to not write against stdout and stderr
    

    if request.method == 'POST':
        
        try:
            _input = request.raw_post_data
            _input = simplejson.loads(request.raw_post_data)
            #print _input['hosts']
        #except JSONDecodeError, e:
            #print "Couldn't parse JSON: %s" % e
        except Exception, e:
            print "Error: %s" % e
                
        try:
            client_url = "http://localhost:8001/tailor/api/v1/schema/"
            client_data = urllib2.urlopen(client_url)
            client_json = client_data.read()
            client_dict = simplejson.loads(client_json)
    
            #Need this?
            from fabric.api import execute
    
            # TODO: dynamically configure the 'env' dict from
            #env = client_dict['env']
            #env.apache_bin_dir = "/etc/init.d/apache2"
            #env.user = 'fabric'
                
            #Set Host via POST Data
            env.hosts = _input['hosts']
            
            file = open("fabric_stuff.py", "w")
            new_string = ""
            new_string = new_string + "from fabric.api import *\nfrom tailor.decorators import *\n\n\nimport fabric\n\n\n"
            
            
            new_string = new_string + '''fabric.state.output["status"] = False\nfabric.state.output["running"] = False\nfabric.state.output["user"] = False\nfabric.state.output["warnings"] = False\nfabric.state.output["stderr"] = False\nfabric.state.output['stdout'] = False\nfabric.state.output['aborts'] = False\n\n'''
            
            
            
            for _varname, _var in client_dict['env'].iteritems():
                if isinstance(_var, str):
                    new_string = new_string + "env.%s = \"%s\"" % (_varname, _var) + "\n"
                else:
                    new_string = new_string + "env.%s = %s" % (_varname, _var) + "\n"
            
            new_string = new_string + "\n\n"
            for dep, dep_func in client_dict['dependencies'].iteritems():
                new_string = new_string + pickle.loads(str(dep_func))
            
            
            new_string = new_string + "\n\n"
            for task, task_func in client_dict['tasks'].iteritems():
                new_string = new_string + pickle.loads(str(task_func))
        
            file.write(new_string)
            file.close()
            import fabric_stuff

            for command in _input['commands']:
                try:
                    execute(eval("fabric_stuff." + command))
                except AttributeError:
                    response_dict = {'success': False, 'message': "Method does not exist."}
                    response = simplejson.dumps(response_dict)
                    return HttpResponse(response, mimetype='application/json', status=400)
            import os
            os.remove("fabric_stuff.py")

            #respond
            response_dict = {'success':True, 'message':"Commands Executed"}
            response = simplejson.dumps(response_dict)
            
            return HttpResponse(response, mimetype='application/json', status=200)
        except Exception, e:
            print "Error: %s" % e
            response_dict = {'success':False, 'message':"Coudn't not execute commands"}
            response = simplejson.dumps(response_dict)
            return HttpResponse(response, mimetype='application/json', status=400)
    else:
        response = "Method is not allow. Only POST is allowed"
        return HttpResponse(response, status=400)



    
