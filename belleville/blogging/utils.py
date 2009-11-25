from datetime import date, datetime

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
        try:
            entry = TumblelogEntry.objects.published().get(slug=slug).title
        except TumblelogEntry.DoesNotExist:
            return None
        cache.set(
            cache_key, 
            entry,
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

from random import randrange, choice
from django.contrib.webdesign.lorem_ipsum import paragraphs, words
from django.template.defaultfilters import slugify
from settings import BloggingSettings
from authors.models import Author
    
class TestData(object):
    """A utility for creating random test data"""
    
    @classmethod
    def create_sample_blog_entries(klass, count=50):
        """
        Create N number of sample blog entries where N = the count parameter.
        Text in posts till be random lorem ipsum text. Author will be a 
        randomly selected author from the system, and date will be a random date
        from the last 2 years. All test entries will be marked "published".
        """
        klass._setup(BlogEntry, count)
        while count > 0:
            headline = words(randrange(3,12), common=False).capitalize()
            slug = klass._check_slug(slugify(headline)[:klass.field_len])
            b = BlogEntry(
                headline = headline,
                slug = slug,
                intro = klass._join_paras(
                    paragraphs(randrange(1,3), common=False)
                ),
                body = klass._join_paras(
                    paragraphs(randrange(2,5), common=False)
                ),
                pub_date = klass._get_rand_date(),
                status = BloggingSettings.PUBLISHED_ENTRY_STATES[0],
                author = Author.objects.order_by('?')[0]
            )
            b.save()
            count += -1
    
    @classmethod
    def create_sample_tumblelog_entries(klass, count=50):
        """
        Create N number of sample tumblelog entries where N = the count 
        parameter. Text in posts till be random lorem ipsum text. Author will be
        a randomly selected author from the system, and date will be a random 
        date from the last 2 years. All test entries will be marked "published".
        """    
        klass._setup(TumblelogEntry, count)
        while count > 0:
            title = words(randrange(3,12), common=False).capitalize()
            slug = klass._check_slug(slugify(title)[:klass.field_len])
            b = TumblelogEntry(
                slug = slug,
                title= title,
                post = klass._join_paras(
                    paragraphs(randrange(1,3), common=False)
                ),
                pub_date = klass._get_rand_date(),
                status = BloggingSettings.PUBLISHED_ENTRY_STATES[0],
                author = Author.objects.order_by('?')[0]
            )
            b.save()
            count += -1    

    @classmethod
    def _setup(klass, model, count):
        klass.slugs = []
        klass.field_len = model._meta.get_field('slug').max_length
        klass.slice_size = klass.field_len - len(str(count)) - 1

    
    @classmethod
    def _check_slug(klass, slug, count=0):
        if slug in klass.slugs:
            slug = slug[:klass.slice_size] + "-%d" % (count + 1)
            return _check_slug(slug, count=(count + 1))
        else:
            klass.slugs.insert(0, slug)
            return slug

    @staticmethod
    def _get_rand_date():
        """Get a random date in the last 2 years"""
        years = [datetime.now().year]
        years.append(years[0] - 1)
        return datetime(
            choice(years),
            randrange(1,12),
            randrange(1,28),
            randrange(1,24),
            randrange(1,60)
        )    

    @staticmethod
    def _join_paras(paras):
        return "\n".join(["<p>%s</p>" % p for p in paras])