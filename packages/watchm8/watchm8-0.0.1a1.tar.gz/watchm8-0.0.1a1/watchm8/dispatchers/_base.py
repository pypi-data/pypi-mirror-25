# -*- coding: utf-8 -*-

from logging import getLogger
from ..event import Subscriber


class BaseDispatcher(Subscriber):

    def __init__(self, actions):
        self._actions = actions
        self._log = getLogger(
            '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        )
