# -*- coding: utf-8 -*-

from ..lib import class_loader


def watcher_factory(watcher):
    if 'kind' not in watcher:
        raise KeyError('Malformed watcher. "kind" parameter missing.')

    if watcher['kind'].startswith('.'):
        watcher['kind'] = 'watchm8.watchers%s' % (watcher['kind'],)

    klass = class_loader(watcher['kind'])
    kwargs = dict(watcher)
    del kwargs['kind']

    return klass(**kwargs)
