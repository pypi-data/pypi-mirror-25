# coding: utf-8
from __future__ import unicode_literals
from copy import deepcopy
import json

from django.utils.safestring import mark_safe
from easy_thumbnails.files import Thumbnailer, ThumbnailOptions
from easy_thumbnails.utils import get_storage_hash
from django.forms.widgets import FileInput

from .cache import get_cache, set_cache, set_cache_by_key, build_key
from .utils.json import CustomJsonEncoder


def ThumbnailOptions__init__(self, *args, **kwargs):
    ThumbnailOptions__init__.old(self, *args, **kwargs)
    for key in ['thumbnail_option_id', 'admin']:
        self.pop(key, None)


def Thumbnailer__get_full_options(self, alias):
    from .models import ThumbnailOption
    from easy_thumbnails.alias import aliases
    options = aliases.get(alias, target=self.alias_target)

    if not options:
        raise KeyError(alias)
    options = deepcopy(options)
    name = self.name
    storage_hash = get_storage_hash(self.storage)
    try:
        override_option = get_cache(alias, name, storage_hash)
        if override_option is None:
            thumbnail_option = ThumbnailOption.objects.get(
                source__name=name,
                source__storage_hash=storage_hash,
                alias=alias)
            set_cache(thumbnail_option)
            override_option = thumbnail_option.options
            override_option['thumbnail_option_id'] = thumbnail_option.id
        options.update(override_option or {})
    except ThumbnailOption.DoesNotExist:
        set_cache_by_key(build_key(alias, name, storage_hash), False)
    return options


def Thumbnailer____getitem__(self, alias):
    """
    Retrieve a thumbnail matching the alias options (or raise a
    ``KeyError`` if no such alias exists).
    """
    options = self.get_full_options(alias)
    return self.get_thumbnail(options, silent_template_exception=True)


def FileInput__render(self, name, value, attrs=None):
    from easy_thumbnails.files import Thumbnailer
    from easy_thumbnails_admin.options import get_options
    is_thumbnailer = isinstance(value, Thumbnailer)
    if is_thumbnailer and value:
        attrs = attrs or {}
        attrs['data-easy-thumbnail-admin-input'] = 1
        attrs['data-name'] = value.name
        attrs['data-target'] = str(value.field)
    rendered = FileInput__render.old(self, name, value, attrs)
    if is_thumbnailer:
        rendered += (
            '<script>'
            'window.easyThumbnailAdminOptions = {};'
            ' </script>'.format(json.dumps(get_options(), ensure_ascii=False, cls=CustomJsonEncoder)))
    return rendered


def FileInput__media(self):
    from ._version import VERSION
    media = FileInput__media.old.fget(self)
    # TODO hash of file
    media.add_js(['easy_thumbnails_admin/js/app.js'])
    return media


def patch():
    Thumbnailer.__getitem__ = Thumbnailer____getitem__
    Thumbnailer.get_full_options = Thumbnailer__get_full_options

    ThumbnailOptions__init__.old = ThumbnailOptions.__init__
    ThumbnailOptions.__init__ = ThumbnailOptions__init__

    FileInput__render.old = FileInput.render
    FileInput.render = FileInput__render

    FileInput__media.old = FileInput.media
    FileInput.media = property(FileInput__media)
