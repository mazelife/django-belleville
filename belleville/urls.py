from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^tumblelog/', include('blogging.tumblelog_urls', namespace="tumblelog")),
    (r'^blog/', include('blogging.blog_urls', namespace="blog")),
    (r'^authors/', include('authors.urls', namespace="authors")),
    (r'^admin/', include(admin.site.urls)),
)
