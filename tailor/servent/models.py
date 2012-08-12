from django.db import models
#from django.contrib.auth.models import User

class Project(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    
    tailor_api = models.CharField(max_length=255, blank=True, default='http://project/tailor/api/v1/schema/')
            
    def __unicode__(self):
        return str(self.name)
