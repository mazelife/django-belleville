from urlparse import urljoin
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.http import Http404
from django.utils.http import urlquote

from site_preferences.utils import get_cached_site_prefs
from settings import MAIN_NAV_REGISTRY

def site_preferences(request):
    """
    A context processor that includes the site_preferences object for the
    current site (e.g. site title, blog and tumblelog settings). To avoid a
    DB lookup for every request, we'll cache site preferences by site ID.
    """
    return {'site_preferences': get_cached_site_prefs()}

def main_nav(request):
    view_func = urlresolvers.resolve(request.path)[0]
    nav_item =  MAIN_NAV_REGISTRY.get(view_func.__module__)
    return {'active_main_nav': nav_item}
    
class Breadcrumb(list):
    """
    A class that extends the standard list type to provide additional help
    to users at the template level.
    """
    @property
    def has_single_crumb(self):
        return self.__len__() == 1

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
    return {
        'breadcrumb': Breadcrumb(zip(urls, breadcrumbs)),
        
    }