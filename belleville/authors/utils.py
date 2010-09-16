from django.core.cache import cache

from project_utils import CacheError
from models import Author

try:
    from settings import SPEEDY_LOOKUP_TTL
except ImportError:
    SPEEDY_LOOKUP_TTL = 60 * 5

def get_cached_author_name(slug=None):
    """
    A function to lookup an author name based on slug. Names are cached to
    avoid unecessary SQL lookups.
    """
    cache_key = 'authors_%s' % slug
    name = cache.get(cache_key)
    if not name:
        try:
            cache.set(
                cache_key, 
                Author.objects.get(slug=slug).__unicode__(), 
                SPEEDY_LOOKUP_TTL
            )
        except Author.DoesNotExist:
            return ""
        name = cache.get(cache_key)
        if not name:
            raise CacheError("Author name could not be cached. Verify that the cache is working.")
    return name