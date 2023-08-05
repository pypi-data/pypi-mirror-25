# -*- coding: utf-8 -*-

from logging import getLogger


class Event(object):

    '''
    Object emitted by watchers reflecting the event produced by observed
    resource.

    Args:
        _type (str): The type of event, eg. created, modified, deleted, ...
            This differs from resource to resource
        data (dict): The raw event data passed to watchers by the observed
            resource
    '''

    def __init__(self, _type, data):
        self._type = _type
        self._data = data

    @property
    def type(self):
        '''The type of event, eg. created, modified, deleted, ...

        Returns:
            str: The event type
        '''
        return self._type

    @property
    def data(self):
        '''The raw event data passed to watchers by the observed resource

        Returns:
            dict: event data
        '''
        return self._data

    def __str__(self):
        return self.type + ': ' + str(self.data)


class EventFan(object):

    def __init__(self, _filter=None):
        self._log = getLogger('EventFan')
        self._subscribers = []
        self._filter = _filter

        self._log.debug('Filter: %s' % _filter.expr)

    def emit(self, event, emitter):
        if self._filter is not None and self._filter(event, emitter) is False:
            self._log.debug('Filtered event %s by %s' % (event, emitter))
            return

        for sub in self._subscribers:
            sub.fire(event, emitter)

    def subscribe(self, sub):
        self._subscribers.append(sub)


class Subscriber(object):

    def fire(self, event, emitter):
        raise NotImplementedError()
