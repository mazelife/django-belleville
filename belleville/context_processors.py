from django.contrib.sites.models import Site

SITE_PREFS_CACHE = {}

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
       