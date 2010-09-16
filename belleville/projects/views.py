from django.shortcuts import get_object_or_404
from django.views.generic import list_detail, simple

from project_utils import annotate, get_page

from models import Project
from utils import get_cached_project_name

@annotate(breadcrumb="Projects")
def project_list(request):
    """A view of a project index page"""
    return list_detail.object_list(request, 
        queryset= Project.objects.published(),
        paginate_by = 20,
        page = get_page(request),
        template_name = 'projects/project_list.html',
        template_object_name = "project"
    )

@annotate(breadcrumb=get_cached_project_name)
def project_detail(request, slug=None):
    """A view of a project"""
    project = get_object_or_404(Project.objects.published(), slug=slug)
    return simple.direct_to_template(request, 
        template="projects/project_detail.html",
        extra_context={'project': project}
    )
