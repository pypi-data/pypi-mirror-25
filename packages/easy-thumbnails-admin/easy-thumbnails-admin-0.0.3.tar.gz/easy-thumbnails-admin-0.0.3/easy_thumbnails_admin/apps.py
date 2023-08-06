from __future__ import unicode_literals

from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    name = 'easy_thumbnails_admin'
    verbose_name = 'Easy thumbnails'

    def ready(self):
        # from .settings import CACHE, STARTUP_CACHE
        # from .cache import rebuild_cache
        from . import monkey_patch
        monkey_patch.patch()

        # TODO check migrations or move to management command
        # if CACHE and STARTUP_CACHE:
        #     rebuild_cache(self.get_model('ThumbnailOption'))

