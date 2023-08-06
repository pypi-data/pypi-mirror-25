# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from .models import ThumbnailOption
from django.contrib.admin.widgets import AdminFileWidget


@admin.register(ThumbnailOption)
class ThumbnailOptionAdmin(admin.ModelAdmin):
    fields = ['source', 'alias', 'options']


class ThumbnailOptionMixin(admin.ModelAdmin):
    class Media:
        pass

    def media(self):
        pass
