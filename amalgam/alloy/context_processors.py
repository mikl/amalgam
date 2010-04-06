# -*- coding: utf-8 -*-
""" Context processors for Amalgam """

from django.conf import settings

def amalgam_settings(request):
    return {'BLOG_SETTINGS': settings.AMALGAM_SETTINGS}

