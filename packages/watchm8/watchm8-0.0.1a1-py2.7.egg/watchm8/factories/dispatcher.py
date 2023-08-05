# -*- coding: utf-8 -*-

from .action import action_factory
from ..dispatchers.core import Sequential as DEFAULT
from ..lib import class_loader


def dispatcher_factory(dispatcher, actions):
    _actions = []

    if type(actions) is list:
        for a in actions:
            _actions.append(action_factory(a))
    else:
        _actions.append(action_factory(actions))

    if dispatcher is None:
        return DEFAULT(_actions)

    if 'kind' not in dispatcher:
        raise KeyError('Malformed dispatcher. "kind" parameter missing.')

    if dispatcher['kind'].startswith('.'):
        dispatcher['kind'] = 'watchm8.dispatchers%s' % (dispatcher['kind'],)

    klass = class_loader(dispatcher['kind'])
    kwargs = dict(dispatcher)
    del kwargs['kind']

    return klass(_actions, **kwargs)
