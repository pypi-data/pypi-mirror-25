# -*- coding: utf-8 -*-

from __future__ import with_statement
from .helpers import Record, rHeap


class Parser:
    def __init__(self):
        self.rheap = rHeap()

    def _enforce_line(self, line):
        arg_list = line.split(' ')
        if len(arg_list) != 2:
            raise Exception('Incorrect input line in document: {}'.format(line))
        try:
            n = int(arg_list[1])
        except ValueError:
            raise Exception('Your value is not a valid integer: {}'.format(line))
        r = Record(uuid=arg_list[0], value=int(arg_list[1]))
        return r


    def scan_document(self, file_path):
        try:
            with open(file_path) as infile:
                for line in infile:
                    record = self._enforce_line(line)
                    self.rheap.push(record)
        except EnvironmentError:
            raise Exception('Could not open your document.')


    def x_largest(self, x):
        try:
            n = int(x)
        except ValueError:
            raise Exception('Your x_largest input is not a valid integer.')
        else:
            x_largest = int(x)
            if x_largest > self.rheap.size():
                raise Exception('X is larger than number of records.')
            elif x_largest < 0:
                raise Exception('X invalidly negative.')
            else:
                return self.rheap.pop_x(x_largest)

