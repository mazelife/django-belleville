from django.core.urlresolvers import reverse
from django.test import TestCase

from models import Author

class AuthorTest(TestCase):

    def test_verify_author_detail_pages(self):
        """
        Verify that each author has a detail page and that the author is 
        contained within the page's context.
        """
        for author in Author.objects.all():
            response = self.client.get(author.get_absolute_url())
            self.assertTrue(response.status_code == 200)
            self.failUnlessEqual(response.context['author'], author)
    
    def test_author_listing(self):
        """
        Verify that the author listing page contains all author names within the
        page's context.
        """
        response = self.client.get(reverse("authors:author_list"))
        self.failUnlessEqual(response.status_code, 200)
        for author in Author.objects.all():
            self.AssertTrue(author in response.context['author_objects'])