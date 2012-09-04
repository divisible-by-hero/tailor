from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from tailor.servent.models import Project

@csrf_exempt    
def fab(request, object_id):
    """
    Accepts JSON (and more later on?) data describing fabric commands
    and runs them if they exist and are allowed.

    #Test it locally
    curl --dump-header - -H "Content-Type:application/json" -H "X_REQUESTED_WITH:XMLHttpRequest" -X POST --data '{"hosts": ["server1.example.com"],"commands": [{"command": "foo","params": []},{"command": "bar","params": []}], "api_key": "geM1hfBV6T4dDrAvzg7XxNM7BQAMCk3I"}' http://localhost:8000/tailor2/api/v1/fab/1
    """
    
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


def projects(request, object_id=None):
    """
    Super, super simple projects api.
    # TODO This is sloppy and has no security. 
    """

    if object_id:
        project = Project.objects.get(id=object_id) 
        instance = {
            "slug": project.slug,
            "tailor_key": project.tailor_key,
            "tailor_api": project.tailor_api,
            "id": project.id,
            "name": project.name
        }
        response = simplejson.dumps(instance)
    else:
        projects = Project.objects.values()
        response = simplejson.dumps(list(projects))    

    return HttpResponse(response, mimetype='application/json', status=200)