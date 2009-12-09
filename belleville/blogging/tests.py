from datetime import datetime, timedelta 

from django.core.urlresolvers import reverse
from django.test import TestCase    

from site_preferences.utils import get_cached_site_prefs

from models import BlogEntry, TumblelogEntry
from settings import BloggingSettings
from authors.models import Author
from utils import TestData

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
        for entry in BlogEntry.objects.published()[:paginate_at]:
            self.assertTrue(entry in response.context['entry_list'])

    def test_archive_lists(self):
        """
        Verify that the blog archive pages work as expected:
        """            
        # Verify that archive index works:
        response = self.client.get(reverse("blog:archive_index"))
        self.failUnlessEqual(response.status_code, 200)
        # Get any random blog's date:
        entry = BlogEntry.objects.published()[1]
        response = self.client.get(reverse("blog:archive_year", kwargs={
            'year': str(entry.pub_date.year)
        }))
        self.failUnlessEqual(response.status_code, 200)
        context = BlogEntry.objects.published().filter(
            pub_date__year=entry.pub_date.year
        )
        for entry in context:
            self.assertTrue(entry in response.context['entry_list'])
        response = self.client.get(reverse("blog:archive_month", kwargs={
            'year': str(entry.pub_date.year),
            'month': str(entry.pub_date.month),
        }))
        self.failUnlessEqual(response.status_code, 200)        
        context = BlogEntry.objects.published().filter(
            pub_date__year=entry.pub_date.year,
            pub_date__month=entry.pub_date.month
        )
        for entry in context:
            self.assertTrue(entry in response.context['entry_list'])
        response = self.client.get(reverse("blog:archive_day", kwargs={
            'year': str(entry.pub_date.year),
            'month': str(entry.pub_date.month),
            'day': str(entry.pub_date.day)
        }))
        self.failUnlessEqual(response.status_code, 200)        
        context = BlogEntry.objects.published().filter(
            pub_date__year=entry.pub_date.year,
            pub_date__month=entry.pub_date.month,
            pub_date__day=entry.pub_date.day           
        )
        for entry in context:
            self.assertTrue(entry in response.context['entry_list'])

            
    def test_entry_detail_pages(self):
        """
        Verify that each entry has a detail page and that the entry is 
        contained within the page's context.
        """
        for entry in BlogEntry.objects.published():
            response = self.client.get(entry.get_absolute_url())
            self.assertTrue(response.status_code == 200)
            try:
                self.failUnlessEqual(response.context['entry'], entry)
            except KeyError:
                self.fail("Template context did not contain entry object.")

    def test_publication_logic(self):
        """
        Verify that unpublished entries cannot be viewed
        """
        unpub_state = filter(
            lambda s: s[0] not in BloggingSettings.PUBLISHED_ENTRY_STATES,
            BloggingSettings.PUB_STATES
        )[0][0]
        pub_state = BloggingSettings.PUBLISHED_ENTRY_STATES[0]
        slug = 'publication-test'
        # Start by creating a new, unpublished entry:
        entry = BlogEntry(
            slug=slug,
            headline='Headline TKTK',
            intro='Loren ipsum...',
            author=Author.objects.all()[0], #any author is fine...
            status=unpub_state,
        )
        entry.save()
        # Trying to view it should show a 404:
        response = self.client.get(entry.get_absolute_url())
        self.assertTrue(response.status_code == 404)
        # Now publish it:
        entry.status = pub_state
        entry.save()
        # Should be visible:
        response = self.client.get(entry.get_absolute_url())
        self.assertTrue(response.status_code == 200)

    def test_comments_logic(self):
        """
        Verify that comments are closed as expected
        """
        pub_state = BloggingSettings.PUBLISHED_ENTRY_STATES[0]
        # Create a published entry, set 'comments_allowed' off:
        entry = BlogEntry(
            slug='test-comments-entry',
            headline='Headline TKTK',
            intro='Loren ipsum...',
            author=Author.objects.all()[0], #any author is fine...
            status=pub_state,
            allow_comments=False
        )
        entry.save()
        self.assertTrue(entry.allow_comments == False)
        entry.allow_comments = True
        entry.save()
        self.assertTrue(entry.comments_enabled)
        # Now set date to just before BloggingSettings.DAYS_COMMENTS_OPEN:
        pd = entry.pub_date - timedelta(BloggingSettings.DAYS_COMMENTS_OPEN + 1)
        entry.pub_date = pd
        entry.save()
        self.assertTrue(entry.comments_enabled == False)

    def test_rss_feed(self):
        """Verify that RSS feed returns a 200"""
        #FIXME: verify that feed has correct context too
        resp= self.client.get(reverse("django.contrib.syndication.views.feed", 
            kwargs={'url': 'blog'}
        ))
        self.failUnlessEqual(resp.status_code, 200)

class TumblelogTest(TestCase):

    fixtures = ['test_data.json']

    def test_entry_list(self):
        """
        Verify that the blog index page contains all blog entry headlines 
        within the page's context.
        """
        response = self.client.get(reverse("tumblelog:list"))
        self.failUnlessEqual(response.status_code, 200)
        paginate_at = get_cached_site_prefs().tumblelog_entries_per_page
        
        try:
             response.context['entry_list']
        except KeyError:
            self.fail("Template context did not contain entry_list object.")
        for entry in TumblelogEntry.objects.published()[:paginate_at]:
            self.assertTrue(entry in response.context['entry_list'])
            
    def test_entry_detail_pages(self):
        """
        Verify that each author has a detail page and that the author is 
        contained within the page's context.
        """
        for entry in TumblelogEntry.objects.published():
            response = self.client.get(entry.get_absolute_url())
            self.assertTrue(response.status_code == 200)
            try:
                self.failUnlessEqual(response.context['entry'], entry)
            except KeyError:
                self.fail("Template context did not contain entry object.")

    def test_publication_logic(self):
        """
        Verify that unpublished entries cannot be viewed
        """
        unpub_state = filter(
            lambda s: s[0] not in BloggingSettings.PUBLISHED_ENTRY_STATES,
            BloggingSettings.PUB_STATES
        )[0][0]
        pub_state = BloggingSettings.PUBLISHED_ENTRY_STATES[0]
        slug = 'publication-test'
        # Start by creating a new, unpublished entry:
        entry = TumblelogEntry(
            slug=slug,
            title='Headline TKTK',
            post='Loren ipsum...',
            author=Author.objects.all()[0], #any author is fine...
            status=unpub_state,
        )
        entry.save()
        # Trying to view it should show a 404:
        response = self.client.get(entry.get_absolute_url())
        self.assertTrue(response.status_code == 404)
        # Now publish it:
        entry.status = pub_state
        entry.save()
        # Should be visible:
        response = self.client.get(entry.get_absolute_url())
        self.assertTrue(response.status_code == 200)
        
    def test_rss_feed(self):
        """Verify that RSS feed returns a 200"""
        #FIXME: verify that feed has correct context too
        resp= self.client.get(reverse("django.contrib.syndication.views.feed", 
            kwargs={'url': 'tumblelog'}
        ))
        self.failUnlessEqual(resp.status_code, 200)       
        
class TestDataGeneration(TestCase):

    def create_test_blog_entries():
        """Create 100 test blog entries"""
        TestData.create_sample_blog_entries(count=100)
        self.assertEqual(BlogEntry.objects.all().count(), 100)        

    def create_test_tumblelogentries():
        """Create 100 test tumblelog entries"""
        TestData.create_sample_tumblelog_entries(count=100)
        self.assertEqual(TumblelogEntry.objects.all().count(), 100)
        
class SiteIndexTest(TestCase):
    
    fixtures = ['test_data.json']
    
    def test_index(self):
        """
        Verify that the site index page contains all blog entries and tumblelog 
        entires within the page's context.
        """
        response = self.client.get(reverse("index"))
        self.failUnlessEqual(response.status_code, 200)
        pg_blog_at = get_cached_site_prefs().blog_entries_per_page
        pg_tumblelog_at = get_cached_site_prefs().tumblelog_entries_per_page 
        try:
             response.context['blog_entry_list']
        except KeyError:
            self.fail((
                "Template context did not contain required blog entry "
                "objects."
            ))
        for entry in BlogEntry.objects.published()[:pg_blog_at]:
            self.assertTrue(entry in response.context['blog_entry_list'])
        try:
             response.context['tumblelog_entry_list']
        except KeyError:
            self.fail((
                "Template context did not contain required tumblelog entry "
                "objects."
            ))
        for entry in TumblelogEntry.objects.published()[:pg_tumblelog_at]:
            self.assertTrue(entry in response.context['tumblelog_entry_list'])        