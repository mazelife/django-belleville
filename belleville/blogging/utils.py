from django.core.cache import cache

from project_utils import CacheError
from models import TumblelogEntry

try:
    from settings import SPEEDY_LOOKUP_TTL
except ImportError:
    SPEEDY_LOOKUP_TTL = 60 * 5

def get_cached_tumblelog_entry_title(slug=None):
    """
    A function to lookup an entry title based on slug. Names are cached to
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
                "Tumblelog entry name could not be cached. Verify that the "
                "cache is working."
            ))
    return name
