# coding: utf-8
from __future__ import unicode_literals

import os
import json
from io import BytesIO

from django.apps import apps
from django.http import JsonResponse

from django.contrib import messages
from django.db.transaction import atomic
from django.forms.models import modelform_factory, modelformset_factory
from functools import partial, wraps

from django.shortcuts import redirect
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.generic import View
from django.views.generic.list import ListView, MultipleObjectMixin

# from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.models import Source, Thumbnail
from easy_thumbnails.alias import aliases
from .models import ThumbnailOption
from .cache import delete_cache


def get_field(target):
    app_label, model_name, field_name = target.split('.')
    model = apps.get_model(app_label, model_name)
    field = model._meta.get_field(field_name)
    return (model, field)


def get_thumbnailer(name, target):
    model, field = get_field(target)
    thumbnailer = getattr(model(**{field.name: name}), field.name)
    # thumbnailer.name = name
    return thumbnailer


class ThumbnailInfoView(View):
    def get(self, request, *args, **kwargs):
        name = self.request.GET['name']
        target = self.request.GET['target']
        thumbnailer = get_thumbnailer(name, target)

        source = thumbnailer.get_source_cache(create=True)
        aliases_dict = {key: thumbnailer.get_full_options(key) for key, opts in aliases.all(target).items()}
        thumbnails = {}
        for key, opt in aliases_dict.items():
            thumbnails[key] = _thumb = {}
            _t = thumbnailer[key]
            _thumb['name'] = _t.name
            _thumb['url'] = _t.url
            _thumb['admin'] = opt.pop('admin', None)
            _thumb['options'] = opt

        data = {
            "id": source.id,
            "name": source.name,
            "url": thumbnailer.url,
            "aliases": aliases_dict,
            "thumbnails": thumbnails
        }
        return JsonResponse(data)


class ThumbnailSetOptionView(View):
    def post(self, request, *args, **kwargs):
        if not request.META.get('CONTENT_TYPE').startswith('application/json'):
            return JsonResponse({"status": "error",
                                 'detail': 'incorrect content-type. need application/json'})
        try:
            data = json.loads(request.body)
        except ValueError as e:
            return JsonResponse({"status": "error", 'detail': e.message})

        name = data['name']
        target = data['target']
        alias = data['alias']
        options = data['options']

        thumbnailer = get_thumbnailer(name, target)
        source = thumbnailer.get_source_cache(create=True)
        t_option, created = ThumbnailOption.objects.get_or_create(
            source=source, alias=alias,
            defaults={'options': options})
        if not created:
            t_option.options = options
            t_option.save(update_fields=['options'])

        delete_cache(t_option)

        options = thumbnailer.get_full_options(alias)
        # options['ALIAS'] = alias

        thumb = thumbnailer[alias]
        storage = thumb.storage
        if storage.exists(thumb.name):
            storage.delete(thumb.name)
        thumbnailer.generate_thumbnail(options)

        return JsonResponse({"status": "ok", "id": t_option.id})


class ThumbnailDeleteOptionView(View):
    def post(self, request, *args, **kwargs):
        if not request.META.get('CONTENT_TYPE').startswith('application/json'):
            return JsonResponse({"status": "error",
                                 'detail': 'incorrect content-type. need application/json'})
        try:
            data = json.loads(request.body)
        except ValueError as e:
            return JsonResponse({"status": "error", 'detail': e.message})

        name = data['name']
        target = data['target']
        alias = data['alias']

        thumbnailer = get_thumbnailer(name, target)
        source = thumbnailer.get_source_cache(create=True)
        ThumbnailOption.objects.filter(source=source, alias=alias).delete()

        thumb = thumbnailer[alias]
        storage = thumb.storage
        if storage.exists(thumb.name):
            storage.delete(thumb.name)
        return JsonResponse({"status": "ok"})
