from django.shortcuts import get_object_or_404
from django.views.generic import list_detail

from models import Author

def author_list(request):
    """A view of all authors"""
    return list_detail.object_list(
        queryset = Author.objects.all(),
        template_name = "authors/author_list.html",
        template_object_name = "author"
    )

def author_detail(request, slug=None):
    """A view of an author"""
    return list_detail.object_detail(
        queryset = Author.objects.all(),
        slug = slug
        template_name = "authors/author_detail.html",
        template_object_name = "author"
    )