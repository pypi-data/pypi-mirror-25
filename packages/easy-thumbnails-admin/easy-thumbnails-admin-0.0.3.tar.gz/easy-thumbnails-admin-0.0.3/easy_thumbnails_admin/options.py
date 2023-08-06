# coding: utf-8
from __future__ import unicode_literals


def get_options():
    from .settings import API_URLS
    return {
        "api": API_URLS
    }