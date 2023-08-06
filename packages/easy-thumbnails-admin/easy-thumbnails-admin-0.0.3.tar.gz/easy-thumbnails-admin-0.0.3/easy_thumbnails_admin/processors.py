# coding: utf-8
from __future__ import unicode_literals

from easy_thumbnails.processors import scale_and_crop as _scale_and_crop


def scale_and_crop(im, size, crop=False, **kwargs):
    if isinstance(crop, dict):
        #
        im = im.crop(map(int, [crop['x'], crop['y'], crop['x'] + crop['width'], crop['y'] + crop['height']]))
        crop = False
    return _scale_and_crop(im, size, crop, **kwargs)
