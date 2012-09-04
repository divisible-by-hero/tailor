__author__ = 'Derek Stegelman'
__date__ = '9/4/12'


import factory
from tailor.servent.models import Project

class ProjectFactory(factory.Factory):
    FACTORY_FOR = Project

    name = 'tailor project'
    slug = 'tailor-project'

