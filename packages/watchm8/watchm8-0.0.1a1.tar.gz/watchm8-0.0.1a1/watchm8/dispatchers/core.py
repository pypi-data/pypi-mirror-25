# -*- coding: utf-8 -*-

from ._base import BaseDispatcher


class Sequential(BaseDispatcher):

    def __init__(self, actions, stop_on_failure=True):
        BaseDispatcher.__init__(self, actions)
        self._stop_on_failure = stop_on_failure

    def fire(self, event, emitter):
        for action in self._actions:
            try:
                action(event, emitter)
            except Exception as e:
                self._log.warning('Action %s failed: %s' % (action, e))

                if self._stop_on_failure is True:
                    self._log.warning('Canceling action dispatcher.')
                    break
