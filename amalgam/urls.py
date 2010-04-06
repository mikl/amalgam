from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

from basic.blog import views as blog_views
from basic.blog.feeds import BlogPostsFeed, BlogPostsByCategory
from basic.blog.sitemap import BlogSitemap

from alloy.feeds import AllEntries, BlogPostsByCategory, BlogPostsFeed, CommentsFeed

admin.autodiscover()

feeds = {
    'all': AllEntries,
    'categories': BlogPostsByCategory,
    'latest': BlogPostsFeed,
    'comments': CommentsFeed,
}

sitemaps = {
    'posts': BlogSitemap,
}

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),

    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),

    url(r'^contact/$', 'alloy.views.contact_form', name='contact_form'),

    url(r'^contact/sent/$', 'django.views.generic.simple.direct_to_template',
        { 'template': 'contact_form/contact_form_sent.html' },
        name='contact_form_sent'),

    url(r'^page/(?P<page>\w)/$', 'alloy.views.index', name='home_paginated'),

    url(r'^$', 'alloy.views.index', name='home_index'),

    url(r'^tags/(?P<slug>[-\w]+)/$', 'alloy.views.tag_detail',
            name='blog_tag_detail'),

    (r'^blog/', include('basic.blog.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
)

if settings.LOCAL_DEV:
    urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)' % settings.MEDIA_URL[1:], 'serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

