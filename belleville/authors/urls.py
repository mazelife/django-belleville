from django.conf.urls.defaults import *

urlpatterns = patterns('authors.views', 
    url(r'^$', "author_list", name="author_list"),
    url(r'^(?P<slug>[\w-]+)/$', "author_detail", name="author_detail")
)    
