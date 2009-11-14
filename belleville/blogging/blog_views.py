from datetime import date

from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import list_detail, date_based, simple

from dizzy.utils import annotate

from models import Entry
from settings import BlogSettings

from utils import get_headline

@annotate(breadcrumb=BlogSettings.TITLE)
def index(request, blog=None):
    """A view of a blog"""
    entries = Entry.published_objects.all()
    return date_based.archive_index(request, 
        queryset= entries,
        date_field = 'pub_date',
        num_latest = BlogSettings.PAGINATE_INDEX_AT,
        template_name = 'blog/index.html',
        extra_context = {'blog': BlogSettings}
    )

@annotate(breadcrumb=get_headline)
def entry_detail(request, year=None, month=None, day=None, slug=None):
    """A view of a blog entry"""
    entry = Entry.published_objects.get(
        pub_date__year=year,
        pub_date__month=month,
        pub_date__day=day,
        slug=slug
    )
    return simple.direct_to_template(request, 
        template="blog/entry_detail.html",
        extra_context={'blog': BlogSettings, 'entry': entry}
    )

@annotate(breadcrumb="Archive")
def archive_index(request, blog=None):
    """
    A view of the years and months on which any blog entry was published
    """
    dates = Entry.published_objects.get_entry_dates()    
    return simple.direct_to_template(request,
        template = 'blog/archive_index.html', 
        extra_context = {
            'dates': dates,
            'blog': BlogSettings
        }
    )

# Date-based archive page viws:

@annotate(breadcrumb=lambda year, month, day: date(int(year), int(month), int(day)).strftime("%e"))
def archive_day(request, year=None, month=None, day=None):
    """A view of posts published on a given day"""  
    return date_based.archive_day(request, 
        queryset=Entry.published_objects.all(),
        template_name="blog/archive_list.html",
        date_field='pub_date',
        year=year,
        month=month, 
        month_format="%m",
        day=day,
        extra_context={'blog': BlogSettings, 
            'archive_type': 'day', 
            'date': date(int(year), int(month), int(day))},
        template_object_name='entry'        
    )

@annotate(breadcrumb=lambda year, month: date(int(year), int(month), 1).strftime("%B"))
def archive_month(request, year=None, month=None):
    """A view of posts published on a given month"""
    return date_based.archive_month(request, 
        queryset=Entry.published_objects.all(),
        template_name="blog/archive_list.html",
        date_field='pub_date',
        year=year,
        month=month, 
        month_format="%m",
        extra_context={'blog': BlogSettings, 
            'archive_type': 'month', 
            'date': date(int(year), int(month), 1)},
        template_object_name='entry'        
    )

@annotate(breadcrumb=lambda year: date(int(year), 1, 1).strftime("%Y"))
def archive_year(request, year=None):
    """A view of posts published in a given year"""     
    return date_based.archive_year(request, 
        queryset=Entry.published_objects.all(),
        template_name="blog/archive_list.html",
        date_field='pub_date',
        year=year,
        extra_context={'blog': BlogSettings, 
            'archive_type': 'year', 
            'date': date(int(year), 1, 1)},
        template_object_name='entry'        
    )