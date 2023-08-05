# -*- coding: utf-8 -*-

from ..lib import class_loader


def action_factory(action):
    if 'kind' not in action:
        raise KeyError('Malformed action. "kind" parameter missing.')

    if action['kind'].startswith('.'):
        action['kind'] = 'watchm8.actions%s' % (action['kind'],)

    klass = class_loader(action['kind'])
    kwargs = dict(action)
    del kwargs['kind']

    return klass(**kwargs)
