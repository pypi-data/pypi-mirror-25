# -*- coding: utf-8 -*-

from collections import namedtuple
from heapq_max import *

Record = namedtuple('Record',[ 'value', 'uuid'])
"""
:param value
:type str
:param uuid
:type int
"""

class rHeap(object):
    """
    This wrapper class holds Record namedtuples in a heap.
    r = Record(uuid, value)

    h = rHeap()
    h.push(Record('1426828011', 9)
    h.pop_x(1)
    """
    def __init__(self):
        self._data = []

    def push(self, record):
        heappush_max(self._data, record)

    def pop_x(self, x):
        x_largest = []
        for i in range(x):
            x_largest.append(heappop_max(self._data).uuid)
        return x_largest

    def size(self):
        return len(self._data)
