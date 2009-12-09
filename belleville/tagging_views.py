from django.shortcuts import get_object_or_404
from django.views.generic import list_detail, simple

from project_utils import annotate, get_page

from site_preferences.utils import get_cached_site_prefs

from tagging.models import Tag, TaggedItem
from tagging.views import tagged_object_list
from blogging.models import BlogEntry, TumblelogEntry

@annotate(breadcrumb="Tags")
def tag_list(request):
    """A view of all tumblelog entires, paginated"""
    tag_list = [(tag, tag.items.count()) for tag in Tag.objects.all()]
    return simple.direct_to_template(request,
        template = "tagging/tag_list.html",
        extra_context = {'tag_list': tag_list}
    )

@annotate(breadcrumb=lambda slug:slug)
def tag_detail(request, slug=None):
    """A view of a tumblelog entry"""
    tag = get_object_or_404(Tag, name=slug)
    tagged_blog_entries = TaggedItem.objects.get_by_model(
        BlogEntry.objects.published(), 
        tag
    )
    tagged_tumblelog_entries = TaggedItem.objects.get_by_model(
        TumblelogEntry.objects.published(), 
        tag
    )
    return simple.direct_to_template(request, 
        template="tagging/tag_detail.html",
        extra_context={
            'tag': tag,
            'blog_entry_list': tagged_blog_entries,
            'tumblelog_entry_list': tagged_tumblelog_entries
        }
    )
