from datetime import date 

from django.core.cache import cache

from project_utils import CacheError
from models import TumblelogEntry, BlogEntry

try:
    from settings import SPEEDY_LOOKUP_TTL
except ImportError:
    SPEEDY_LOOKUP_TTL = 60 * 5

def get_cached_tumblelog_entry_title(slug=None):
    """
    A function to lookup an BlogEntry title based on slug. Names are cached to
    avoid unecessary SQL lookups.
    """
    cache_key = 'tumblelog_entry_%s' % slug
    name = cache.get(cache_key)
    if not name:
        cache.set(
            cache_key, 
            TumblelogEntry.objects.published().get(slug=slug).title,
            SPEEDY_LOOKUP_TTL
        )
        name = cache.get(cache_key)
        if not name:
            raise CacheError((
                "Tumblelog BlogEntry name could not be cached. Verify that the "
                "cache is working."
            ))
    return name

def get_cached_blog_entry_headline(
    year=None, 
    month=None, 
    day=None, 
    slug=None):
    """
    A function to lookup a blog BlogEntry headline based on it's slug. Headlines are
    cached to avoid unecessary SQL lookups that are necessitated by the ORM
    machinery.
    """
    pub_date = date(int(year), int(month), int(day)).isoformat()
    cache_key = "blog_entry_%s_%s" % (pub_date, slug)
    name = cache.get(cache_key)
    if not name:
        entry = BlogEntry.objects.get(
            pub_date__year=year,
            pub_date__month=month,
            pub_date__day=day,
            slug=slug
        )
        cache.set(cache_key, entry.headline, SPEEDY_LOOKUP_TTL)
        name = cache.get(cache_key)
        if not name:
            raise CacheError((
            "Blog BlogEntry headline could not be cached. "
            "Verify that the cache is working."
            ))
    return name        