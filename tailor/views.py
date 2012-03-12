import pickle
import inspect
import simplejson
import urllib2
import sys

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings as djangosettings
from django.views.decorators.csrf import csrf_exempt
from tailor.stitch import Sew
from fabric.api import *

from tailor.decorators import tailored

def schema(request):
    '''
    Parses the project fabfile and returns API listing
    the available commands.  Commands are made available by
    adding the @tailored (name?) decorator to a fabric function.
    '''

    if request.REQUEST.get('key'):
        if request.REQUEST.get('key') in djangosettings.TAILOR_API_KEYS.values():

            #The directory that hold the fabfile needs to be added to the python path
            # TODO: Make this configurable
            from conf import fabfile
    
            fab_props = dir(fabfile)
                        
            include_list = ['env']
            good_props = []
            for p in fab_props:
                if hasattr( eval('fabfile.%s' % p), 'tailored' ) or \
                    hasattr( eval('fabfile.%s' % p), 'dependency' ) or \
                    p in include_list:
                        good_props.append(p)

            fab_dict = {}
            fab_tasks = []
            fab_dependencies = []
            fab_dict['tasks'] = fab_tasks
            fab_dict['dependencies'] = fab_dependencies
    
            for prop in good_props:
                # If it's a callable, pickle it
                if hasattr( eval('fabfile.%s' % prop), '__call__' ):
                    if hasattr( eval('fabfile.%s' % prop), 'tailored' ):
                        task = {}
                        _callable = eval('fabfile.%s' % prop)
                        callable_source = inspect.getsource(_callable)
                        task['name'] = prop
                        task['task'] = (pickle.dumps(callable_source))
                        task['docstring'] = _callable.__doc__
                        fab_tasks.append(task)
                    elif hasattr( eval('fabfile.%s' % prop), 'dependency' ):
                        task = {}
                        _callable = eval('fabfile.%s' % prop)
                        callable_source = inspect.getsource(_callable)
                        task['name'] = prop
                        task['task'] = (pickle.dumps(callable_source))
                        task['docstring'] = _callable.__doc__
                        fab_dependencies.append(task)

                # Else just use the value
                else:
                    fab_dict[prop] = eval('fabfile.%s' % prop)
    
            response = simplejson.dumps(fab_dict)    
            return HttpResponse(response, mimetype='application/json', status=200)

        else:
            return HttpResponse("API Key Not Recognized", status=403)
    else:
        return HttpResponse("API Key Required", status=403)


@csrf_exempt    
def fab(request):
    '''
    Accepts JSON (and more later on?) data describing fabric commands
    and runs them if they exist and are allowed.

    #Test it locally
    curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"hosts": ["server1.example.com"],"commands": ["alpha", "kick_apache"], "api_key": "geM1hfBV6T4dDrAvzg7XxNM7BQAMCk3I", "schema_url": "http://localhost:8001/tailor/api/v1/schema/"}' http://localhost:8001/tailor/api/v1/fab/

    # NOTE: This is all PoC at this point.  Lots of hard-coded values
    # TODO: Seperate all this out to methods
    '''
    
    import fabric

    # Turn off output as to not write against stdout and stderr
    

    if request.method == 'POST':
        
        try:
            _input = request.raw_post_data
            _input = simplejson.loads(request.raw_post_data)
            api_key = _input['api_key']
            schema_url = _input['schema_url']
            #print _input['hosts']
        #except JSONDecodeError, e:
            #print "Couldn't parse JSON: %s" % e
        except Exception, e:
            print "Error: %s" % e
                
        try:
            print api_key
            print schema_url
            client_url = "%s?key=%s" % (schema_url, api_key)
            print client_url
            client_data = urllib2.urlopen(client_url)
            client_json = client_data.read()
            client_dict = simplejson.loads(client_json)
            print "YO"
            env.hosts = _input['hosts']
            
            sewing = Sew()
            sewing.setup()
            sewing.add_vars(client_dict['env'])
            sewing.add_methods(client_dict['dependencies'].iteritems())
            sewing.add_methods(client_dict['tasks'].iteritems())
            result = sewing.execute(_input['commands'])
            sewing.cleanup()
            if result:    
                response_dict = {'success':True, 'message':"Commands Executed"}
                response = simplejson.dumps(response_dict)
            
                return HttpResponse(response, mimetype='application/json', status=200)
            else:
                response_dict = {'success':False, 'message':"Coudn't not execute commands"}
                response = simplejson.dumps(response_dict)
                return HttpResponse(response, mimetype='application/json', status=400)
        except Exception, e:
            print "Error: %s" % e
            response_dict = {'success':False, 'message':"Coudn't not execute commands"}
            response = simplejson.dumps(response_dict)
            return HttpResponse(response, mimetype='application/json', status=400)
    else:
        response = "Method is not allow. Only POST is allowed"
        return HttpResponse(response, status=400)



    
