import simplejson

#from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from tailor.servent.models import Project

@csrf_exempt    
def fab(request, object_id):
    '''
    Accepts JSON (and more later on?) data describing fabric commands
    and runs them if they exist and are allowed.

    #Test it locally
    curl --dump-header - -H "Content-Type:application/json" -H "X_REQUESTED_WITH:XMLHttpRequest" -X POST --data '{"hosts": ["server1.example.com"],"commands": [{"command": "foo","params": []},{"command": "bar","params": []}], "api_key": "geM1hfBV6T4dDrAvzg7XxNM7BQAMCk3I"}' http://localhost:8000/tailor2/api/v1/fab/1

    # NOTE: This is all PoC at this point.  Lots of hard-coded values
    # TODO: Seperate all this out to methods
    '''
    
    if request.method == 'POST':
        try:
            _input = request.raw_post_data
            _input = simplejson.loads(request.raw_post_data)
            project = Project.objects.get(id=object_id)
            return project.run_fab(_input)            
        except Exception, e: # TODO: Better exception handling
            print "Error: %s" % e
    else:
        response = "Method is not allow. Only POST is allowed"
        return HttpResponse(response, status=400)
