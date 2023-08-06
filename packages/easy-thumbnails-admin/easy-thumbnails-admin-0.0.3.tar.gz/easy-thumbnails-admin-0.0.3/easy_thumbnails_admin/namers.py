# coding: utf-8
from __future__ import unicode_literals



from easy_thumbnails.namers import default as _default, alias


def default(thumbnailer, prepared_options, thumbnail_options, source_filename,
            thumbnail_extension, **kwargs):
    if thumbnail_options.get("ALIAS"):
        return alias(thumbnailer, thumbnail_options, source_filename, thumbnail_extension, **kwargs)
    return _default(thumbnailer, prepared_options, source_filename, thumbnail_extension, **kwargs)
