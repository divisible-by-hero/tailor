from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from tailor.deployment import *

def schema(request):
    '''
    Parses the project fabfile and returns API listing
    the available commands.  Commands are made available by
    adding the @tailored (name?) decorator to a fabric function.
    '''
    try:
        fabfile = settings.TAILOR_FABRIC_PATH
    except:
        print "Define TAILOR_FABRIC_PATH in settings"
        #raise Exception('Define TAILOR_FABRIC_PATH in settings')
    
    ##parse parse parse
    ##psuedocode
    command_list = []
    command1 = { 'command':'alpha', 'kwargs': []}  #kwargs would prob have to be dict, not list (keyword, default value)
    command2 = { 'command':'make_release', 'kwargs': ['tag','message']}
    command_list.append(command1)
    command_list.append(command2)
    
    #serialize
    #make it json for now, xml and more later
    response = simplejson.dumps(command_list)
    
    return HttpResponse(response, mimetype='application/json', status=200)
    
def endpoint(request):
    '''
    Accepts JSON (and more later on?) data describing fabric commands
    and runs them if they exist and are allowed.
    '''
    
    commands = request.raw_post_data
    
    #parse, parse, parse commands
    
    #psuedocode
    #execute, execute, execute
    try:
        #for command in commands:
            #command(this,that,things,stuff)
        
        response_dict = {'success':True, 'message':"Commands Executed"}
        response = simplejson.dumps(response_dict)
        return HttpResponse(response, mimetype='application/json', status=200)
    except:
        response_dict = {'success':False, 'message':"Coudn't not execute commands"}
        response = simplejson.dumps(response_dict)
        return HttpResponse(response, mimetype='application/json', status=400)
    
    
def command(request, command):
    ''' Execute Given Command '''
    if command == "deploy":
        result, text_response = alpha_deploy("errors")
    else:
        result, text_response = alpha_rebuild("errors")
    if result:
        response = HttpResponse(text_response, status=200)
    else:
        response = HttpResponse("Error", status=500)
    
    return response
    