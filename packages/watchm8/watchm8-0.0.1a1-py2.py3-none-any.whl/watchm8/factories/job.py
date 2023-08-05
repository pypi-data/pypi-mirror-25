# -*- coding: utf-8 -*-

from .watcher import watcher_factory
from .dispatcher import dispatcher_factory
from ..job import Job
from .._filter import Filter


def job_factory(job):
    for k in ('watch', 'do'):
        if k not in job:
            raise KeyError('Malformed job. "%s" parameter missing.' % k)

    watchers = []
    if type(job['watch']) is list:
        for w in job['watch']:
            watchers.append(watcher_factory(w))
    else:
        watchers.append(watcher_factory(job['watch']))

    if 'dispatcher' in job:
        dispatcher = dispatcher_factory(job['dispatcher'], job['do'])
    else:
        dispatcher = dispatcher_factory(None, job['do'])

    _filter = None
    if 'filter' in job and job['filter'] is not None:
        _filter = Filter(job['filter'])

    return Job(watchers, _filter, dispatcher)
