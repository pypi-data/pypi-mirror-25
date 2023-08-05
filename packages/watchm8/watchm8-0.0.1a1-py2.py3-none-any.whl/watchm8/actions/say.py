# -*- coding: utf-8 -*-

from ._base import BaseAction

'''
.. module:: say
   :synopsis: Actions purely for debugging or logging events

.. moduleauthor:: Simon Pirschel <simon@aboutsimon.com>
'''


class Event(BaseAction):

    '''Log event to info level

    Example:
        .. code-block:: yaml

            do:
                kind: .say.Event
    '''

    def __call__(self, event, emitter):
        self._log.info(str(event))
