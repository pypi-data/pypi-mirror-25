# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy

DEFAULT_API_URLS = {
    "detail": reverse_lazy('easy_thumbnail_admin:detail'),
    "set-option": reverse_lazy('easy_thumbnail_admin:set-option'),
    "delete-option": reverse_lazy('easy_thumbnail_admin:delete-option'),
}

SETTINGS = {
    "API_URLS": DEFAULT_API_URLS,
    "CACHE": "default",
    "CACHE_TIMEOUT": 60 * 60 * 24,  # cache 24 hours
    "STARTUP_CACHE": True,
}

SETTINGS.update(dict(getattr(settings, 'EASY_THUMBNAILS_ADMIN', {})))

API_URLS = SETTINGS['API_URLS']
CACHE = SETTINGS['CACHE']
CACHE_TIMEOUT = SETTINGS['CACHE_TIMEOUT']
STARTUP_CACHE = SETTINGS['STARTUP_CACHE']
