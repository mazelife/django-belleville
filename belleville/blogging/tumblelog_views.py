from django.shortcuts import get_object_or_404
from django.views.generic import list_detail, simple

#from dizzy.utils import annotate

from models import TumblelogEntry
from settings import BloggingSettings

#from utils import get_headline

    
#@annotate(breadcrumb=BlogSettings.TITLE)
def entry_list(request):
    """A view of all tumblelog entires, paginated"""
    current_page = get_page(request)
    return list_detail.object_list(
        queryset = TumblelogEntry.objects.published,
        paginate_by  = BloggingSettings.PAGINATE_TUMBLELOG_INDEX_AT,
        page = current_page
        template_name = "blogging/tumblelog_entry_list.html",
        template_object_name = "entry"
    )

#@annotate(breadcrumb=get_headline)
def entry_detail(request, slug=None):
    """A view of a tumblelog entry"""
    entry = get_object_or_404(TumblelogEntry.objects.published, slug=slug)
    return simple.direct_to_template(request, 
        template="blog/tumblelog_entry_detail.html",
        extra_context={'entry': entry}
    )

def get_page(request):
    """
    Not a view function, just a utility to get the page number from a request 
    object.
    """
    page = request.GET.get('page', '1')
    if page.isdigit():
        return int(page)
    return 1
