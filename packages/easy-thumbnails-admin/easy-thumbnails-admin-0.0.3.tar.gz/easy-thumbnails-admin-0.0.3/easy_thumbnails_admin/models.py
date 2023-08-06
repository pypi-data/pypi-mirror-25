# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from jsonfield import JSONField


class ThumbnailOption(models.Model):
    source = models.ForeignKey('easy_thumbnails.Source', related_name='options', on_delete=models.CASCADE)
    alias = models.CharField(max_length=42)
    options = JSONField(blank=True, null=True)

    class Meta:
        unique_together = ['source', 'alias']

    def get_cleaned_options(self):
        keys = ['crop']
        new_options = {}
        for key, value in self.options.items():
            if key in keys:
                new_options[key] = value
        return new_options


@receiver(post_save, sender=ThumbnailOption)
def option_save(sender, instance, **kwargs):
    from .cache import set_cache
    set_cache(instance)


@receiver(post_delete, sender=ThumbnailOption)
def option_delete(sender, instance, **kwargs):
    from .cache import delete_cache
    delete_cache(instance)
