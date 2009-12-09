from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse

from site_preferences.utils import get_cached_site_prefs

from models import BlogEntry, TumblelogEntry
from settings import BloggingSettings as BSet

class BlogFeed(Feed):
    "%s: %s" % (
        get_cached_site_prefs().site_title,
        get_cached_site_prefs().blog_title
    )
    link = reverse("blog:entry_list")
    description = "Updates to the blog."

    def items(self):
        return BlogEntry.objects.published()[:BSet.ITEMS_IN_FEED]

class TumblelogFeed(Feed):
    "%s: %s" % (
        get_cached_site_prefs().site_title,
        get_cached_site_prefs().tumblelog_title
    )
    link = reverse("tumblelog:list")
    description = "Updates to the tumblelog."

    def items(self):
        return TumblelogEntry.objects.published()[:BSet.ITEMS_IN_FEED]
