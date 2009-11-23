from django.conf.urls.defaults import *

urlpatterns = patterns('blogging.blog_views', 
    url(r'^$', 'entry_list', name="entry_list"),
    url(r'^archive/?$', 'archive_index', name="archive_index"), 
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w-]+)/$', 'entry_detail', name="entry_detail"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'archive_day', name="archive_day"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive_month', name="archive_month"),
    url(r'^(?P<year>\d{4})/$', 'archive_year', name="archive_year"),
)    