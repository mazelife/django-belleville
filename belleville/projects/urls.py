from django.conf.urls.defaults import *

urlpatterns = patterns('projects.views', 
    url(r'^$', "project_list", name="list"),
    url(r'^(?P<slug>[\w-]+)/$', "project_detail", name="detail")
)    
