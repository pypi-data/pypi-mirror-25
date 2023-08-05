# -*- coding: utf-8 -*-

from . import watchers
from . import actions


class Watchm8(object):

    def __init__(self, config):
        self._config = config

        from logging import getLogger
        self._jobs = []
        self._log = getLogger('Watchm8')
        self._stop_watchm8 = False

    def start(self):
        from .factories.job import job_factory  # don't pollute namespace

        self._log.info('Starting ...')

        for job in self._config['jobs']:
            self._jobs.append(job_factory(job))

        self._log.debug('Created jobs')

        self.run()

    def run(self):
        from time import sleep  # don't pollute namespace

        self._log.debug('Starting jobs')

        # start all jobs
        for job in self._jobs:
            job.start()

        self._log.info('Started.')

        while not self._stop_watchm8:
            sleep(3)

        self._log.info('Stopping ...')

        # Stopping jobs
        for job in self._jobs:
            job.stop()

        # Joining job threads
        for job in self._jobs:
            job.join()

        self._log.info('Stopped.')

    def stop(self):
        self._stop_watchm8 = True
