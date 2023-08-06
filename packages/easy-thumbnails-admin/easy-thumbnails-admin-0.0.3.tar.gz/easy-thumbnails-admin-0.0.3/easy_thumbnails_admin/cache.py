# coding: utf-8
from __future__ import unicode_literals

from hashlib import sha256

from django.core.cache import caches
from django.utils.encoding import smart_bytes

from .settings import CACHE, CACHE_TIMEOUT
from .utils.queryset import queryset_iterator

CACHE_PREFIX = 'easy_thumbnails_admin:'

cache = caches[CACHE]


def build_key(alias, name, storage_hash):
    key_str = smart_bytes("{alias}_{name}_{storage_hash}".format(alias=alias, name=name, storage_hash=storage_hash))
    return '%s%s' % (CACHE_PREFIX, sha256(key_str).hexdigest())


def build_key_from_instance(thumbnail_option):
    return build_key(thumbnail_option.alias, thumbnail_option.source.name, thumbnail_option.source.storage_hash)


def set_cache(thumbnail_option, timeout=CACHE_TIMEOUT):
    key = build_key_from_instance(thumbnail_option)
    options = thumbnail_option.options
    options['thumbnail_option_id'] = thumbnail_option.id
    cache.set(key, options, timeout)


def set_cache_by_key(key, value, timeout=CACHE_TIMEOUT):
    cache.set(key, value, timeout)


def delete_cache(thumbnail_option):
    key = build_key_from_instance(thumbnail_option)
    cache.delete(key)


def get_cache(alias, name, storage_hash):
    key = build_key(alias, name, storage_hash)
    return cache.get(key)


def rebuild_cache(ThumbnailOption):
    # TODO flush all keys by prefix
    for to in queryset_iterator(ThumbnailOption.objects.select_related('source').order_by('pk')):
        set_cache(to)
