from django.core.urlresolvers import reverse
from django.views.generic import simple

from project_utils import annotate

from site_preferences.utils import get_cached_site_prefs

from blogging.models import TumblelogEntry, BlogEntry
from blogging.settings import BloggingSettings



@annotate(breadcrumb=get_cached_site_prefs().site_title)
def index(request):
    """A view of the site index page"""
    tumblelogs_per_page = get_cached_site_prefs().tumblelog_entries_per_page
    tumbelelog_entry_list = TumblelogEntry.objects.published()[:tumblelogs_per_page]
    tumblelog_next_page = reverse("tumblelog:list") + "?page=2"
    blogs_per_page = get_cached_site_prefs().blog_entries_per_page
    blog_entry_list = BlogEntry.objects.published()[:blogs_per_page]    
    blog_next_page = reverse("blog:entry_list") + "?page=2"
    return simple.direct_to_template(request, 
        template = 'index.html',
        extra_context = {
            'tumblelog_entry_list': tumbelelog_entry_list,
            'tumblelog_next_page_link': tumblelog_next_page,
            'blog_entry_list': blog_entry_list,
            'blog_next_page_link': blog_next_page
        }
    )