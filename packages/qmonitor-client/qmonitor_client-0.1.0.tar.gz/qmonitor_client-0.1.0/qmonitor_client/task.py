#!/usr/bin/python
from __future__ import unicode_literals

import os
import time
import datetime
import threading
import glob

from . import core


class _ClearAll(threading.Thread):
    def __init__(self, interval, registry=core.REGISTRY):
        super(_ClearAll, self).__init__()
        self._interval = interval
        self._registry = registry

    def run(self):
        is_done = False
        while True:
            # reset at the last 5 second of every minute
            second = datetime.datetime.now().second
            if not is_done and second >= 55:
                is_done = True
                if 'qmonitor_multiproc_dir' in os.environ:
                    path = os.environ.get('qmonitor_multiproc_dir')
                    for f in glob.glob(os.path.join(path, '*.db')):
                        parts = os.path.basename(f).split('_')
                        typ = parts[0]
                        if typ == 'summary':
                            d = core._MmapedDict(f)
                            d.clear_value()

                for collector in self._registry._collector_to_names:
                    for metric in collector.collect():
                        if metric.type == 'summary':
                            collector.reset()
                            break

            elif is_done and second < 55:
                is_done = False
            time.sleep(1)


class _ClearMemory(threading.Thread):
    def __init__(self, interval, registry=core.REGISTRY):
        super(_ClearMemory, self).__init__()
        self._interval = interval
        self._registry = registry

    def run(self):
        is_done = False
        while True:
            # reset at the last 5 second of every minute
            second = datetime.datetime.now().second
            if not is_done and second >= 55:
                is_done = True
                for collector in self._registry._collector_to_names:
                    for metric in collector.collect():
                        if metric.type == 'summary':
                            collector.reset()
                            break

            elif is_done and second < 55:
                is_done = False
            time.sleep(1)



class ClearAllTask(object):
    def __init__(self, registry=core.REGISTRY):
        self._registry = registry
        self._start()

    def _start(self, interval=60.0):
        t_clear = _ClearAll(interval, self._registry)
        t_clear.daemon = True
        t_clear.start()


class ClearMemoryTask(object):
    def __init__(self, registry=core.REGISTRY):
        self._registry = registry
        self._start()

    def _start(self, interval=60.0):
        t_clear = _ClearMemory(interval, self._registry)
        t_clear.daemon = True
        t_clear.start()
