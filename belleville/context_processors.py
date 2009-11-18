from urlparse import urljoin
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.http import Http404
from django.utils.http import urlquote

SITE_PREFS_CACHE = {} # FIXME: This should use the low-level caching framework.

def site_preferences(request):
    """
    A context processor that includes the site_preferences object for the
    current site (e.g. site title, blog and tumblelog settings). To avoid a
    DB lookup for every request, we'll cache site preferences by site ID.
    """
    site = Site.objects.get_current()
    try:
        site_prefs = SITE_PREFS_CACHE[site.id]
    except KeyError:
        site_prefs = site.preference
        SITE_PREFS_CACHE[site.id] = site_prefs
    return {'site_preferences': site_prefs}

def breadcrumb(request):
    """
    A context processor that returns a context variable representing a breadcrumb
    """
    try:
        from settings import BREADCRUMB_IGNORE_PATH
    except ImportError:
       BREADCRUMB_IGNORE_PATH = None
    urls = []
    def parseURL(url):
        """recursively shorten url"""
        if url != "/":
            urls.insert(0, url)
            parseURL(urljoin(url, '..'))
    path = BREADCRUMB_IGNORE_PATH and request.path.replace(BREADCRUMB_IGNORE_PATH, '') or request.path
    parseURL(path)
    #get view for specified url
    resolver = urlresolvers.get_resolver(None)
    breadcrumbs = []
    crumblessViews = []   
    for url in urls:
        try:
            callback, callback_args, callback_kwargs = resolver.resolve(url)
        except Http404:
            #URL does not have a view, which means no breadcrumb either
            crumblessViews.append(url)                
        else:
            #Check if view has a breadcrumb property
            crumb = getattr(callback, 'breadcrumb', None)
            if crumb:
                #if the breadrumb is a callable object, call it, passing kwargs...
                crumb = hasattr(crumb, '__call__') and crumb.__call__(**callback_kwargs) or crumb
                #if not, just append to the list of breadcrumbs
                breadcrumbs.append(crumb)
            else:
                #...otherwise, add to urls with no breadcrumb
                crumblessViews.append(url)
    [urls.remove(url) for url in crumblessViews]
    if BREADCRUMB_IGNORE_PATH:
        urls = [BREADCRUMB_IGNORE_PATH + url for url in urls]
    return {'breadcrumb': zip(urls, breadcrumbs)}       