# coding: utf-8
from __future__ import unicode_literals

import gc


def queryset_iterator(queryset, chunk_size=1000):
    """
    Iterate over a Django Queryset ordered by the primary key
    This method loads a maximum of chunk_size (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.
    Note that the implementation of the iterator does not support ordered query sets.
    """
    i = 0
    while True:
        qs = list(queryset.filter()[chunk_size * i:chunk_size * (i + 1)])
        if not qs:
            break
        for row in qs:
            yield row
        i += 1
        gc.collect()
