from urlparse import urljoin
from django.core import urlresolvers
from django.utils.http import urlquote

def annotate(**kwargs):
    """
    A decorator which annotates a function with properties specified in the key-
    word arguments. Used by the breadcrumb middleware.
    """
    def _wrapped_view_func(fn):
        for property, value in kwargs.items():
            setattr(fn, property, value)
        return fn
    return _wrapped_view_func

class CacheError(Exception):
    """
    An exception which will be raised when Django's low-level cache framework
    doesn't seem to work (probably becuase it's not configured by the user).
    """
    # Fixme: let the user they need to turn caching on
    pass

def get_page(request, param_name="page"):
    """
    A utility to get the page number from a request 
    object.
    """
    page = request.GET.get(param_name, '1')
    if page.isdigit():
        return int(page)
    return 1

# Startup Registry: adds a way to register a function to be called once,
# when the app starts up

class StartupHookRegistryFactory(object): 

    _registry = []
    
    def register(self, f):
        assert hasattr(f, '__call__'), (
            "Items registered to the startup registry must be callable."
            "%s is not." % f.__repr__()
            )
        self._registry.append(f)
    
    def activate(self):
        [f.__call__() for f in self._registry]
        
StartupHookRegistry = StartupHookRegistryFactory()

from django import template
StartupHookRegistry.register(
    lambda: template.add_to_builtins(
        'django.contrib.humanize.templatetags.humanize'
    )
)

