from django import http
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import list_detail

from basic.blog.models import Post, Category
from contact_form.views import contact_form as django_contact_form
from contact_form.forms import ContactForm
from django_proxy.models import Proxy
from honeypot.decorators import check_honeypot
from basic.blog.models import Post, Category
from tagging.models import Tag, TaggedItem


def index(request, page=0, template_name='proxy/proxy_list_front.html', **kwargs):
    '''
    Homepage.

    Template: ``proxy/proxy_list_front.html``
    Context:
        object_list
            Aggregated list of Proxy instances (post, quote, bookmark).

    '''
    posts = Proxy.objects.published().order_by('-pub_date')

    return list_detail.object_list(
        request,
        queryset = posts,
        paginate_by = 10,
        page = page,
        template_name = template_name,
        **kwargs
    )


def tag_detail(request, slug, template_name='proxy/tag_detail.html', **kwargs):
    ''' Display objects for all content types supported: Post and Quotes.'''

    tag = get_object_or_404(Tag, name__iexact=slug)

    #below could be prettier
    results = []
    qs = Proxy.objects.published().filter(tags__icontains=tag.name).order_by('-pub_date')
    for item in qs:
        comma_delimited = (',' in item.tags)
        if comma_delimited:
            for t in item.tags.split(','):
                if t.strip(' ') == tag.name:
                    results.append(item)
        else:
            for t in item.tags.split(' '):
                if t.strip(' ') == tag.name:
                    results.append(item)

    return render_to_response(template_name,
                    {'tag': tag, 'object_list': results},
                    context_instance=RequestContext(request),
                    )

@check_honeypot
def contact_form(request, form_class=ContactForm,
                 template_name='contact_form/contact_form.html'):

    '''
    Handles the contact form view. Leverages django-contact-form.

    This is an example of overriding another reusable apps view. This particular
    view also contains a form. For this example we are just doing the basic
    implementation by wrapping the view function and simply passing the
    arguments along.

    This view is also leveraging another reusable app, django-honeypot. The
    decorator you see being applied is used to protect your app from spam.
    '''
    return django_contact_form(request, form_class=form_class,
                 template_name=template_name)

