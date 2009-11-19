from django.conf.urls.defaults import *

urlpatterns = patterns('blogging.tumblelog_views', 
    url(r'^$', "tumblelog_entry_list", name="list"),
    url(r'^(?P<slug>[\w-]+)/$', "tumblelog_entry_detail", name="detail")
)    