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

def make_sample_posts(count=50):
    """
    This is a convinience function to quickly generate a bunch of sample
    blog posts with random loren ipsum text and dates. The count parameter
    specifies how many posts to generate.
    """
    from datetime import datetime
    from random import randrange, choice
    from django.contrib.webdesign.lorem_ipsum import paragraphs, words
    from django.template.defaultfilters import slugify
    from models import BlogEntry
    from settings import BloggingSettings
    from authors.models import Author
    
    slice_size = 50 - len(str(count)) - 1
    slugs = []
    def check_slug(slug, count=0):
        if slug in slugs:
            slug = slug[:slice_size] + "-%d" % (count + 1)
            return check_slug(slug, count=(count + 1))
        else:
            slugs.insert(0, slug)
            return slug
    def join_paras(paras):
        return "\n".join(["<p>%s</p>" % p for p in paras])
    while count > 0:
        headline = words(randrange(3,12), common=False).capitalize()
        slug = check_slug(slugify(headline)[:50])
        b = BlogEntry(
            headline = headline,
            slug = slug,
            intro = join_paras(paragraphs(randrange(1,3), common=False)),
            body = join_paras(paragraphs(randrange(2,5), common=False)),
            pub_date = datetime(
                choice([2009, 2008]),
                randrange(1,12),
                randrange(1,30),
                randrange(1,24),
                randrange(1,60)
            ),
            status = BloggingSettings.PUBLISHED_ENTRY_STATES[0],
            author = Author.objects.order_by('?')[0]
        )
        b.save()
        count += -1    