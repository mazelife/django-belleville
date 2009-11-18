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
