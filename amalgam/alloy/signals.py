""" Configure signals """

from django.db.models import signals
from django_proxy.signals import proxy_save, proxy_delete
from basic.blog.models import Post
#from quoteme.models import Quote
from basic.bookmarks.models import Bookmark

# Since we don't want to fork django-basic-apps, we attach the ProxyMeta
# classes by way of monkeypatching.
class PostProxyMeta:
    title = 'title'
    description = 'body'
    tags = 'tags'
    pub_date = 'publish'
    active = {'status':2}
Post.ProxyMeta = PostProxyMeta

class BookmarkProxyMeta:
    title = 'title'
    description = 'description'
    tags = 'tags'
Bookmark.ProxyMeta = BookmarkProxyMeta

signals.post_save.connect(proxy_save, Post, True)
signals.post_delete.connect(proxy_delete, Post)

#signals.post_save.connect(proxy_save, Quote, True)
#signals.post_delete.connect(proxy_delete, Quote)

signals.post_save.connect(proxy_save, Bookmark, True)
signals.post_delete.connect(proxy_delete, Bookmark)

