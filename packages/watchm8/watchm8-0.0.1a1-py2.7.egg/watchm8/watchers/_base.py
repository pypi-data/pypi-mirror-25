# -*- coding: utf-8 -*-

from logging import getLogger
from threading import Thread


class _BaseWatcher(object):

    def __init__(self):
        self._log = getLogger(
            '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        )

    def set_fan(self, event_fan):
        self._fan = event_fan

    def _emit(self, event):
        self._fan.emit(event, self)


class BaseWatcher(_BaseWatcher, Thread):

    def __init__(self):
        _BaseWatcher.__init__(self)
        Thread.__init__(self)
        self._stop_watcher = False

    def _run(self):
        raise NotImplementedError()

    def run(self):
        self._log.info('Starting watcher')
        self._run()
        self._log.info('Exiting watcher')

    def stop(self):
        self._log.info('Stopping watcher')
        self._stop_watcher = True
