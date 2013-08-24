from django.utils import unittest

from tailor.servent.tests.factories import ProjectFactory

__author__ = 'Derek Stegelman'
__date__ = '9/4/12'


class ProjectTestCase(unittest.TestCase):

    def setUp(self):
        self.project = ProjectFactory.create()

    def test_name(self):
        self.assertEqual(self.project.slug, "tailor-project")


