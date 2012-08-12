import pickle
import inspect
import simplejson
import urllib2
import sys
import imp
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings as djangosettings
from django.views.decorators.csrf import csrf_exempt

from fabric.api import *

from tailor.servent.stich import Sew

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
        print request.raw_post_data
        
        try:
            _input = request.raw_post_data
            _input = simplejson.loads(request.raw_post_data)
            api_key = _input['api_key']
            schema_url = _input['schema_url']
        except Exception, e:
            print "Error: %s" % e
                
        try:
            client_url = "%s?key=%s" % (schema_url, api_key)
            client_data = urllib2.urlopen(client_url)
            client_json = client_data.read()
            client_dict = simplejson.loads(client_json)
            env.hosts = _input['hosts']
            
            sewing = Sew()
            sewing.setup()
            sewing.add_vars(client_dict['env'])
            sewing.add_methods(client_dict['dependencies'])
            sewing.add_methods(client_dict['tasks'])
            result, response_list = sewing.execute(_input['commands'])
            sewing.cleanup()
            if result:    
                response_dict = {'success':True, 'message':"Commands Executed", 'responses': response_list}
                print response_dict
                #from django.core import serializers
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
