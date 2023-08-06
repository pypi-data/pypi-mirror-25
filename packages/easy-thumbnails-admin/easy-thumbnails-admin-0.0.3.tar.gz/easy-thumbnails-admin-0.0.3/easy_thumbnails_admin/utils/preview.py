# coding: utf-8
from __future__ import unicode_literals

from operator import attrgetter

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from easy_thumbnails.exceptions import InvalidImageFormatError


def build_image_preview(field,
                         alias=None, options=None,
                         verbose_name=None,
                         clickable=True,
                         no_label=False):
    get_image = attrgetter(field)

    options = options or {
        'size': (100, 100),
    }

    def image_preview(self, obj):
        image = get_image(obj)
        html = '&mdash;'
        try:
            if image:
                if options:
                    preview = image.get_thumbnail(thumbnail_options=options)
                if alias:
                    preview = image[alias]

                tag = ('<img class="image-thumbnail" width="{preview.width}"'
                       ' src="{preview.url}">'.format(preview=preview))

                if clickable:
                    tag = (
                        '<a href="{image.url}" '
                        'target="_blank">'
                        '{tag}'
                        '</a>'.format(image=image, tag=tag)
                    )
                html = tag
        except (IOError, InvalidImageFormatError) as e:
            html = '&mdash;e! <!-- {} -->'.format(e)

        return ('<div '
                'style="display: flex; align-items: center; justify-content: center;">'
                '{html}'
                '</div>'.format(html=html)
                )

    image_preview.allow_tags = True
    if no_label:
        image_preview.short_description = ''
    else:
        if verbose_name:
            image_preview.short_description = verbose_name
        else:
            image_preview.short_description = field
    return image_preview
