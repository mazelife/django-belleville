from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'site_index.index', name="index"),
    (r'^tumblelog/', include('blogging.tumblelog_urls', namespace="tumblelog")),
    (r'^blog/', include('blogging.blog_urls', namespace="blog")),
    (r'^authors/', include('authors.urls', namespace="authors")),
    (r'^projects/', include('projects.urls', namespace="projects")),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^search/', 'pierre.site_search.views.index'),
    url(r'^tags/$', 'tagging_views.tag_list', name="tag_list"),
    url(r'^tags/(?P<slug>[\w-]+)/$', 'tagging_views.tag_detail', name="tag_detail"),
    (r'^admin/', include(admin.site.urls)),
)


from blogging.feeds import BlogFeed, TumblelogFeed

feeds = {
    'blog': BlogFeed,
    'tumblelog': TumblelogFeed,
}

urlpatterns += patterns('', 
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),
)
