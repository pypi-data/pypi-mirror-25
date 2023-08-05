# -*- coding: utf-8 -*-

from logging import getLogger
from time import sleep
from threading import Thread
from watchm8.event import EventFan


class Job(Thread):

    def __init__(self, watchers, _filter, dispatcher):
        Thread.__init__(self)

        self._watchers = watchers
        self._filter = _filter
        self._dispatcher = dispatcher

        self._log = getLogger('Job')
        self._fan = EventFan(self._filter)
        self._stop_job = False

    @property
    def watchers(self):
        return self._watchers

    @property
    def dispatcher(self):
        return self._dispatcher

    def run(self):
        self._log.info('Starting job')

        # Subscribe dispatcher to event fan
        self._fan.subscribe(self._dispatcher)

        # Assign event fan to all watchers
        for w in self.watchers:
            w.set_fan(self._fan)

        self._log.info('Starting watchers')
        # Start all watchers
        for w in self.watchers:
            w.start()

        self._log.info('Job started')
        # Main loop
        while not self._stop_job:
            sleep(3)

        self._log.info('Stopping watchers')

        # Stop all watchers
        for w in self.watchers:
            w.stop()

        for w in self.watchers:
            w.join()

        self._log.info('Job stopped')

    def stop(self):
        self._stop_job = True
