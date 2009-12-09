from datetime import date

from django.contrib.humanize.templatetags.humanize import ordinal
from django.core import urlresolvers
from django.shortcuts import get_object_or_404
from django.views.generic import list_detail, date_based, simple


from project_utils import annotate, get_page
from site_preferences.utils import get_cached_site_prefs

from models import BlogEntry
from settings import BloggingSettings
from utils import get_cached_blog_entry_headline

@annotate(breadcrumb=get_cached_site_prefs().blog_title)
def entry_list(request):
    """A view of a blog index page"""
    return list_detail.object_list(request, 
        queryset= BlogEntry.objects.published(),
        paginate_by = get_cached_site_prefs().blog_entries_per_page,
        page = get_page(request),
        template_name = 'blogging/blog_entry_list.html',
        template_object_name = "entry"
    )

@annotate(breadcrumb=get_cached_blog_entry_headline)
def entry_detail(request, year=None, month=None, day=None, slug=None):
    """A view of a blog entry"""
    entry = get_object_or_404(BlogEntry.objects.published(),
        pub_date__year=year,
        pub_date__month=month,
        pub_date__day=day,
        slug=slug
    )
    admin_url = urlresolvers.reverse(
        'admin:blogging_blogentry_change', 
        args=(entry.id,)
    )
    return simple.direct_to_template(request, 
        template="blogging/blog_entry_detail.html",
        extra_context={'entry': entry, 'admin_url': admin_url}
    )

@annotate(breadcrumb="Archive")
def archive_index(request, blog=None):
    """
    A view of the years and months on which any blog entry was published
    """
    dates = BlogEntry.objects.get_entry_dates()    
    return simple.direct_to_template(request,
        template = 'blogging/blog_archive_index.html', 
        extra_context = {
            'dates': dates,
        }
    )

# Date-based archive page views:

@annotate(breadcrumb=lambda year, month, day: 
    ordinal(date(int(year), int(month), int(day)).strftime("%e")))
def archive_day(request, year=None, month=None, day=None):
    """A view of posts published on a given day"""  
    return date_based.archive_day(request, 
        queryset=BlogEntry.objects.published(),
        template_name="blogging/blog_archive_list.html",
        date_field='pub_date',
        year=year,
        month=month, 
        month_format="%m",
        day=day,
        extra_context={
            'archive_type': 'day', 
            'date': date(int(year), int(month), int(day))},
        template_object_name='entry'
    )

@annotate(breadcrumb=lambda year, month: date(int(year), \
    int(month), 1).strftime("%B"))
def archive_month(request, year=None, month=None):
    """A view of posts published on a given month"""
    return date_based.archive_month(request, 
        queryset=BlogEntry.objects.published(),
        template_name="blogging/blog_archive_list.html",
        date_field='pub_date',
        year=year,
        month=month, 
        month_format="%m",
        extra_context={
            'archive_type': 'month', 
            'date': date(int(year), int(month), 1)},
        template_object_name='entry'        
    )

@annotate(breadcrumb=lambda year: date(int(year), 1, 1).strftime("%Y"))
def archive_year(request, year=None):
    """A view of posts published in a given year"""     
    return date_based.archive_year(request, 
        queryset=BlogEntry.objects.published(),
        template_name="blogging/blog_archive_list.html",
        date_field='pub_date',
        year=year,
        make_object_list=True,
        extra_context={
            'archive_type': 'year', 
            'date': date(int(year), 1, 1)},
        template_object_name='entry'        
    )