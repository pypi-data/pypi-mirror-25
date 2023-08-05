#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# File: notifierlib.py
"""
Main module file

Put your classes here
"""

import logging
import abc

from stopit import ThreadingTimeout, TimeoutException
from Queue import Queue
from threading import Thread

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = 'plaintext'
__date__ = '''18-09-2017'''

# This is the main prefix used for logging
LOGGER_BASENAME = '''notifierlib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

WORKERS = 3
TIMEOUT = 30


class Channel(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._logger = logging.getLogger('{base}.{suffix}'
                                         .format(base=LOGGER_BASENAME,
                                                 suffix=self.__class__.__name__)
                                         )

    @abc.abstractmethod
    def notify(self):
        pass


class Group(object):
    def __init__(self, groupname='', *channels):
        self._logger = logging.getLogger('{base}.{suffix}'
                                         .format(base=LOGGER_BASENAME,
                                                 suffix=self.__class__.__name__)
                                         )
        self.name = groupname
        self._channels = [self._validate_channel(channel)
                          for channel in channels]
        self._queue = Queue()
        self._results = None

    @staticmethod
    def _validate_channel(channel):
        if not isinstance(channel, Channel):
            raise ValueError('The object is not a Channel')
        return channel

    def _start_workers(self):
        for _ in range(WORKERS):
            worker = Thread(target=self._worker, args=(self._queue,))
            worker.setDaemon(False)
            worker.start()

    def __call__(self, **kwargs):
        self.send(**kwargs)

    def send(self, **kwargs):
        self._results = []
        for channel in self._channels:
            self._queue.put((channel, kwargs))
        self._start_workers()
        self._logger.debug('Waiting for results')
        self._queue.join()
        self._logger.debug(('Result of notification: '
                            '{result}').format(result=self._results))
        return self._results

    def _worker(self, queue):
        while not queue.empty():
            channel, kwargs = queue.get()
            self._logger.debug(('Sending notification using channel: {channel} '
                                'with args:{args}').format(channel=channel.name,
                                                           args=kwargs))
            try:
                with ThreadingTimeout(TIMEOUT):
                    result = channel.notify(**kwargs)
                    self._results.append({channel.name: result})
            except TimeoutException:
                self._logger.error(('The worker reached the time limit '
                                    '({} secs)').format(TIMEOUT))
            except Exception:
                self._logger.exception(('Exception caught on sending on '
                                        'channel:{}').format(channel.name))
            queue.task_done()


class Notifier(object):
    def __init__(self):
        self._logger = logging.getLogger('{base}.{suffix}'
                                         .format(base=LOGGER_BASENAME,
                                                 suffix=self.__class__.__name__)
                                         )
        self.broadcast = Group('broadcast')

    @property
    def channels(self):
        return [channel.name for channel in self.broadcast._channels]  # noqa

    def register(self, *args):
        for channel in args:
            if not isinstance(channel, Channel):
                raise ValueError(('The object is not a Channel :'
                                  '[{}]').format(channel))
            if channel.name in self.channels:
                raise ValueError('Channel already registered')
            self.broadcast._channels.append(channel)  # noqa

    def unregister(self, *args):
        for channel in args:
            if channel.name not in self.channels:
                raise ValueError('Channel not registered')
            self.broadcast._channels = [ch for ch in self.broadcast._channels  # noqa
                                        if not ch.name == channel.name]

    def add_group(self, group):
        if not isinstance(group, Group):
            raise ValueError(('The object is not a Group :'
                              '[{}]').format(group))
        setattr(self, group.name, group)

    def remove_group(self, group):
        if not isinstance(group, Group):
            raise ValueError(('The object is not a Group :'
                              '[{}]').format(group))
        try:
            delattr(self, group.name)
            return True
        except AttributeError:
            self._logger.error('No such group :{}'.format(group.name))
            return False
