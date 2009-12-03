from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse

from site_preferences.utils import get_cached_site_prefs

from models import BlogEntry, TumblelogEntry

class BlogFeed(Feed):
    "%s: %s" % (
        get_cached_site_prefs().site_title,
        get_cached_site_prefs().blog_title
    )
    link = reverse("blog:entry_list")
    description = "Updates to the blog."

    def items(self):
        return BlogEntry.objects.published()[:20]

class TumblelogFeed(Feed):
    "%s: %s" % (
        get_cached_site_prefs().site_title,
        get_cached_site_prefs().tumblelog_title
    )
    link = reverse("tumblelog:list")
    description = "Updates to the tumblelog."

    def items(self):
        return TumblelogEntry.objects.published()[:20]
