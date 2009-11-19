from django.conf.urls.defaults import *

urlpatterns = patterns('blogging.views', 
    url(r'^$', "tumblelog_list"),
    url(r'^(?P<slug>[\w-]+)/$', "tumblelog_detail")
)    