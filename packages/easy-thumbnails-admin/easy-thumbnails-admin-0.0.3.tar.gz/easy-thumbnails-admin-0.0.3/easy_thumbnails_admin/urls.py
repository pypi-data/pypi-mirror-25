# coding: utf-8
from __future__ import unicode_literals

from django.conf.urls import url, include

from . import views

api_patterns = [
    url(r'^detail/$', views.ThumbnailInfoView.as_view(), name='detail'),
    url(r'^set-option/$', views.ThumbnailSetOptionView.as_view(), name='set-option'),
    url(r'^delete-option/$', views.ThumbnailDeleteOptionView.as_view(), name='delete-option'),
]

urlpatterns = [
    url('^', include(api_patterns, namespace='easy_thumbnail_admin'))
]
