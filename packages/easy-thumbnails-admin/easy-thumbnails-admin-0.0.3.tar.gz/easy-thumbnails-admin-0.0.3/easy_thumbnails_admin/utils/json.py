# coding: utf-8
from __future__ import unicode_literals
from django.core.serializers.json import DjangoJSONEncoder


class CustomJsonEncoder(DjangoJSONEncoder):
    def default(self, o):
        if hasattr(o, '__class__') and o.__class__.__name__ == '__proxy__':
            return str(o)
        return DjangoJSONEncoder.default(self, o)
