from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Atom1Feed
from django.conf import settings
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site

from basic.blog.models import Post, Category
from django_proxy.models import Proxy


class BlogPostsFeed(Feed):
    title = '%s blog feed' % settings.AMALGAM_SETTINGS['site_name']
    subtitle =  settings.AMALGAM_SETTINGS['site_slogan']
    author_name = settings.AMALGAM_SETTINGS['author_name']
    copyright = settings.AMALGAM_SETTINGS['copyright']
    feed_type = Atom1Feed

    def link(self):
        return reverse('blog_index')

    def items(self):
        return Post.objects.published().order_by('-publish')[:10]

    def item_pubdate(self, obj):
        return obj.publish


class BlogPostsByCategory(Feed):
    title = '%s blog category feed' % settings.AMALGAM_SETTINGS['site_name']
    author_name = settings.AMALGAM_SETTINGS['author_name']
    copyright = settings.AMALGAM_SETTINGS['copyright']
    feed_type = Atom1Feed

    def get_object(self, bits):
        if len(bits) != 1:
            raise FeedDoesNotExist
        return Category.objects.get(slug__exact=bits[0])

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return "Posts recently categorized as %s" % obj.title

    def items(self, obj):
        # Temporary date filter to prevent repost of old content to blog
        # aggregation sites.
        from datetime import date

        return obj.post_set.published().filter(publish__gt=date(2010, 04, 01)).order_by('-publish')[:10]

    def item_pubdate(self, obj):
        return obj.publish


class CommentsFeed(Feed):
    title = '%s comment feed' % settings.AMALGAM_SETTINGS['site_name']
    feed_type = Atom1Feed

    def link(self):
        return reverse('blog_index')

    def items(self):
        ctype = ContentType.objects.get_for_model(Post)
        return Comment.objects.filter(content_type=ctype).order_by('-submit_date')[:10]

    def item_pubdate(self, obj):
        return obj.submit_date


class AllEntries(Feed):
    title = '%s all entries feed' % settings.AMALGAM_SETTINGS['site_name']
    subtitle =  settings.AMALGAM_SETTINGS['site_slogan']
    author_name = settings.AMALGAM_SETTINGS['author_name']
    copyright = settings.AMALGAM_SETTINGS['copyright']
    feed_type = Atom1Feed

    def link(self):
        current_site = Site.objects.get(id=settings.SITE_ID)
        return 'http://%s' % current_site.domain

    def items(self):
        return Proxy.objects.published().order_by('-pub_date')[:10]

    def item_link(self, item):
        return item.content_object.get_absolute_url()

    def item_categories(self, item):
        return item.tags.replace(',', '').split()

    def item_pubdate(self, item):
        return item.pub_date

