# -*- coding: utf-8 -*-

from logging import getLogger


class JobFailed(Exception):
    '''Exception raised if actions in Job failed.'''


class BaseAction(object):

    '''Base class for actions, every action must inherit from BaseAction

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    '''

    def __init__(self, *args, **kwargs):
        self._log = getLogger(
            '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        )

    def __call__(self, event, emitter):
        '''Abstract method

        Args:
            event (:obj:`watchm8.event.RawEvent`): Event produced by watcher
            emitter (:obj:`watchm8.watchers._base._BaseWatcher`): Watcher
        '''
        raise NotImplementedError()
