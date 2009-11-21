from django.shortcuts import get_object_or_404
from django.views.generic import list_detail, simple

from project_utils import annotate, get_page

from site_preferences.utils import get_cached_site_prefs

from models import TumblelogEntry
from settings import BloggingSettings
from utils import get_cached_tumblelog_entry_title

@annotate(breadcrumb=get_cached_site_prefs().tumblelog_title)
def tumblelog_entry_list(request):
    """A view of all tumblelog entires, paginated"""
    return list_detail.object_list(request,
        queryset = TumblelogEntry.objects.published(),
        paginate_by  = get_cached_site_prefs().tumblelog_entries_per_page,
        page = get_page(request),
        template_name = "blogging/tumblelog_entry_list.html",
        template_object_name = "entry"
    )

@annotate(breadcrumb=get_cached_tumblelog_entry_title)
def tumblelog_entry_detail(request, slug=None):
    """A view of a tumblelog entry"""
    entry = get_object_or_404(TumblelogEntry.objects.published(), slug=slug)
    return simple.direct_to_template(request, 
        template="blogging/tumblelog_entry_detail.html",
        extra_context={'entry': entry}
    )

