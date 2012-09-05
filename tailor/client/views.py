import pickle
import inspect
import urllib2
import sys
import imp
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings as djangosettings
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

from fabric.api import *

def schema(request):
    """
    Parses the project fabfile and returns API listing
    the available commands.  Commands are made available by
    adding the @tailored decorator to a fabric function.
    """

    if request.REQUEST.get('key'):
        if request.REQUEST.get('key') in djangosettings.TAILOR_API_KEYS.values():

            # TODO: Handle for ImportErrors and dynamically find and load
            # any modules the fabfile requires
            
            # Load the fabfile and add its dir to sys.path
            fabfile_directory = os.path.dirname(djangosettings.TAILOR_FABFILE_PATH)
            sys.path.append(fabfile_directory)
            try:
                fabfile = imp.load_source('fabfile', djangosettings.TAILOR_FABFILE_PATH)
            except ImportError, e:
                print e
    
            # Complile list properties to be included in api
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

            # Build dict of fabric tasks and properties
            for prop in good_props:
                #If Fabric Task
                if hasattr( eval('fabfile.%s' % prop), 'tailored' ):
                    fab_tasks.append(parse_function(prop, fabfile))
                elif hasattr( eval('fabfile.%s' % prop), 'dependency' ):
                    fab_dependencies.append(parse_function(prop, fabfile))
                # Else just use the value
                else:
                    fab_dict[prop] = eval('fabfile.%s' % prop)
    
            response = simplejson.dumps(fab_dict)    
            return HttpResponse(response, mimetype='application/json', status=200)

        else:
            return HttpResponse("API Key Not Recognized", status=403)
    else:
        return HttpResponse("API Key Required", status=403)


def parse_function(prop, fabfile):
    """
    Accepts a callable property of the fabfile,
    parses it and returns a dictionary describing the
    fabric task function.
    """
    task = {}
    _callable = eval('fabfile.%s' % prop)
    callable_source = inspect.getsource(_callable)
    
    
    task['name'] = prop
    task['task'] = (pickle.dumps(callable_source))
    task['docstring'] = _callable.__doc__

    #arguments, defaults
    argspecs = inspect.getargspec(_callable)
    arguments = []
    for index, argument in enumerate(argspecs.args):
        _argument = {}
        _argument['arg'] = argument
        if argspecs.defaults:
            diff = (len(argspecs.args) - len(argspecs.defaults))
        else:
            diff = -1
        if argspecs.defaults and index >= diff:
            _argument['default'] = argspecs.defaults[index - diff]
        arguments.append(_argument)
    task['arguments'] = arguments

    # *args and *kwargs
    if argspecs.varargs:
        task['varargs'] = True
    else:
        task['varargs'] = False

    if argspecs.keywords:
        task['kwargs'] = True
    else:
        task['kwargs'] = False

    return task