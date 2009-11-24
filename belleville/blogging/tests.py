from django.core.urlresolvers import reverse
from django.test import TestCase    

from site_preferences.utils import get_cached_site_prefs

from models import BlogEntry, TumblelogEntry
from settings import BloggingSettings
from authors.models import Author

class BlogTest(TestCase):

    fixtures = ['test_data.json']

    def test_entry_list(self):
        """
        Verify that the blog index page contains all blog entry headlines 
        within the page's context.
        """
        response = self.client.get(reverse("blog:entry_list"))
        self.failUnlessEqual(response.status_code, 200)
        paginate_at = get_cached_site_prefs().blog_entries_per_page
        
        try:
             response.context['entry_list']
        except KeyError:
            self.fail("Template context did not contain entry_list object.")
        for entry in BlogEntry.objects.published()[:paginate_at]
            self.assertTrue(entry in response.context['entry_list'])
            
    def test_entry_detail_pages(self):
        """
        Verify that each author has a detail page and that the author is 
        contained within the page's context.
        """
        for entry in BlogEntry.objects.published():
            response = self.client.get(author.get_absolute_url())
            self.assertTrue(response.status_code == 200)
            try:
                self.failUnlessEqual(response.context['entry'], entry)
            except KeyError:
                self.fail("Template context did not contain entry object.")

    def test_publication_logic(self):
        """
        Verify that unpublished entries cannot be viewed
        """
        upub_state = filter(
            BloggingSettings.PUB_STATES, 
            lambda s: s[0] not in BloggingSettings.PUBLISHED_ENTRY_STATES
        )[0][0]
        pub_state = BloggingSettings.PUBLISHED_ENTRY_STATES[0]
        slug = 'publication-test'
        # Start by creating a new, unpublished entry:
        entry = BlogEntry(
            slug=slug,
            headline='Headline TKTK',
            intro='Loren ipsum...',
            author=Author.objects.all()[0] #any author is fine...
            status=upub_state,
        )
        entry = entry.save()
        # Trying to view it should show a 404:
        response = self.client.get(entry.get_absolute_url())
        self.assertTrue(response.status_code == 404)
        # Now publish it:
        entry.status = pub_state
        entry = entry.save()
        # Should be visible:
        response = self.client.get(entry.get_absolute_url())
        self.assertTrue(response.status_code == 200)