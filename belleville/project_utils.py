from urlparse import urljoin
from django import forms
from django.conf import settings
from django.core import urlresolvers
from django.template.loader import render_to_string
from django.utils.http import urlquote
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

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

class CKEditor(forms.Textarea):
    """A richtext editor widget that uses CKEditor.
    Inspired by http://code.google.com/p/django-ck
    """
    class Media:
        js = (
            getattr(settings, 'CKEDITOR_PATH', 'scripts/ckeditor/ckeditor.js'),
        )

    def __init__(self, *args, **kwargs):
        self.ck_attrs = kwargs.get('ck_attrs', {})
        if self.ck_attrs:
            kwargs.pop('ck_attrs')
        super(CKEditor, self).__init__(*args, **kwargs)
        
    def serialize_script_params(self):
        ck_attrs = ''
        if not 'language' in self.ck_attrs:
            self.ck_attrs['language'] = get_language()[:2]
        for k,v in self.ck_attrs.iteritems():
            ck_attrs += k + " : '" + v + "',"
        return ck_attrs
    
    def render(self, name, value, attrs=None):
        #import pdb; pdb.set_trace()
        rendered = super(CKEditor, self).render(name, value, attrs)
        ck_attrs = self.serialize_script_params()
        return render_to_string('ckeditor_object.html', {
            'basepath': settings.MEDIA_URL + "scripts/ckeditor/",
            'field': rendered,
            'field_name': name,
            'options': mark_safe(ck_attrs),
        })

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

from pierre import site_search
StartupHookRegistry.register(site_search.autodiscover)