from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from models import Author

class AuthorTest(TestCase):

    fixtures = ['test_data.json']

    def test_author_listing(self):
        """
        Verify that the author listing page contains all author names within the
        page's context.
        """
        response = self.client.get(reverse("authors:list"))
        self.failUnlessEqual(response.status_code, 200)
        try:
             response.context['author_list']
        except KeyError:
            self.fail("Template context did not contain author_list object.")
        for author in Author.objects.all():
            self.assertTrue(author in response.context['author_list'])
            
    def test_verify_author_detail_pages(self):
        """
        Verify that each author has a detail page and that the author is 
        contained within the page's context.
        """
        for author in Author.objects.all():
            response = self.client.get(author.get_absolute_url())
            self.assertTrue(response.status_code == 200)
            try:
                self.failUnlessEqual(response.context['author'], author)
            except KeyError:
                self.fail("Template context did not contain author object.")
    
    def test_author_repr(self):
        """
        Verify that authors are represented correctly, even when user has no 
        first  or last name.
        """
        new_user = User.objects.create_user('testusername', 't@t.com', 'pass')
        new_user.save()
        new_author = Author(user=new_user, slug="testusername")
        new_author.save()
        # If no user first/last name, show username:
        self.failUnlessEqual(new_author.__unicode__(), 'testusername')
        new_user.first_name = "Test"
        new_user.last_name = "User"
        new_user.save()
        # Now shoudl be full name:
        self.failUnlessEqual(new_author.__unicode__(), 'Test User')