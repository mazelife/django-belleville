from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from models import Project

class ProjectsTest(TestCase):

    fixtures = ['test_data.json']

    def test_project_listing(self):
        """
        Verify that the project listing page contains all projects within the
        page's context.
        """
        response = self.client.get(reverse("projects:list"))
        self.failUnlessEqual(response.status_code, 200)
        try:
             response.context['project_list']
        except KeyError:
            self.fail("Template context did not contain project_list object.")
        for project in Project.objects.published():
            self.assertTrue(project in response.context['project_list'])
            
    def test_verify_author_detail_pages(self):
        """
        Verify that each author has a detail page and that the author is 
        contained within the page's context.
        """
        for project in Project.objects.all():
            response = self.client.get(project.get_absolute_url())
            if project.published():
                self.assertTrue(response.status_code == 200)
                try:
                    self.failUnlessEqual(response.context['project'], project)
                except KeyError:
                    self.fail("Template context did not contain project object.")

            else:
                self.assertTrue(response.status_code == 404)
