#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from importlib import import_module


def load_class(cls):
    """
    :param str cls:     Class name to load.
    :returns class:     Class that has been loaded.
    """
    module_name, class_name = cls.rsplit(".", 1)
    module = import_module(module_name)
    return getattr(module, class_name)


def string_2_bool(value):
    """
    :param str value: value to convert to bool

    :raise ValueError: when value is not one of the possible values [0, 1, True, False, true, false]

    :returns bool: True or False
    """

    value = str(value).lower()
    if value.isdigit():
        return bool(int(value))
    elif value == 'true':
        return True
    elif value == 'false':
        return False
    else:
        raise ValueError('Invalid value for expected bool')


def show_statistics(res=None):
    import resource

    res = res or resource.RUSAGE_SELF
    usage = resource.getrusage(res)

    for name, desc in [
        ('ru_utime', 'User time'),
        ('ru_stime', 'System time'),
        ('ru_maxrss', 'Max. Resident Set Size'),
        ('ru_ixrss', 'Shared Memory Size'),
        ('ru_idrss', 'Unshared Memory Size'),
        ('ru_isrss', 'Stack Size'),
        ('ru_inblock', 'Block inputs'),
        ('ru_oublock', 'Block outputs'),
    ]:
        print '%-25s (%-10s) = %s' % (desc, name, getattr(usage, name))


class PercentageFile(object):
    def __init__(self, filename):
        self.size = os.stat(filename)[6]
        self.delivered = 0
        self.f = file(filename)

    def read(self, size=None):
        if size is None:
            self.delivered = self.size
            return self.f.read()

        data = self.f.read(size)
        self.delivered += len(data)
        return data

    @property
    def percentage(self):
        return float(self.delivered) / self.size * 100.0

    def show_percentage(self):
        print self.percentage
