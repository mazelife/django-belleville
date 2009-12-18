from django.core.cache import cache

from project_utils import CacheError
from django.contrib.sites.models import Site

try:
    from settings import SPEEDY_LOOKUP_TTL
except ImportError:
    SPEEDY_LOOKUP_TTL = 60 * 60

def get_cached_site_prefs(slug=None):
    """
    A function to lookup an site prefs, which are cached to
    avoid unecessary SQL lookups.
    """
    site = Site.objects.get_current()
    site_prefs = cache.get(str(site.id))
    if not site_prefs:
        cache.set(
            str(site.id), 
            site.preference,
            SPEEDY_LOOKUP_TTL
        )
        site_prefs = cache.get(str(site.id))
        if not site_prefs:
            raise CacheError((
            "Site prefs could not be cached."
            "Verify that the cache is configured and working."
        ))
    return site_prefs