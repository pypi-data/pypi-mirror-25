# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, print_function, absolute_import


# TODO -- move proxi implementation into here

class Upstart(object):
    def start(self):
        raise NotImplementedError()

    def restart(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def is_running(self):
        raise NotImplementedError()
