from django.shortcuts import render
from tailor.deployment import *
from django.http import HttpResponse

    
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
    