# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from sqlalchemy.orm import scoped_session

try:
    import threading
except ImportError as e:
    import dummy_threading as threading

from sqlalchemy import MetaData
from .registry import RoutedSession
from sqlalchemy.orm import sessionmaker
from modelchemy import dbs


class RequestSessionFactory(object):
    _session = None
    _session_factory = None

    def __init__(self, init=None):

        if init is None:
            init = {}

        def callback():
            return scoped_session(
                sessionmaker(class_=RoutedSession, registry=dbs)
            )

        self._session_factory = callback

        self.storage = threading.local()
        self.storage.lazies = {}
        self.storage.concrete = {}
        self.storage.metadatas = {}
        self.lazies.update(init)

    @property
    def Session(self):
        if self._session is None:
            self._session = self.SessionFactory()
        return self._session

    @property
    def SessionFactory(self):
        return self._session_factory

    @property
    def lazies(self):
        return self.storage.lazies

    @property
    def concrete(self):
        return self.storage.concrete

    @property
    def lookup(self):
        return self.storage.metadatas

    def register(self, key, sessionmaker, metadata=None):
        self.lazies[key] = sessionmaker
        if metadata is not None:
            if isinstance(metadata, MetaData):
                self.lookup[key] = metadata

    def close(self):

        if self._session is not None:
            self._session.close()

        for key in self.lazies.keys():
            if key in self.concrete:
                session = self.concrete.get(key)
                close_key = "close"
                if hasattr(session, close_key):
                    close_callable = getattr(session, close_key)
                    if callable(close_callable):
                        close_callable()

    def __getattr__(self, attr):
        if attr == 'lazies':
            return self.storage.lazies

        if attr == 'concrete':
            return self.storage.concrete

        if attr == 'lookup':
            return self.storage.metadatas

        if attr not in self.lazies.keys():
            raise AttributeError("Invalid attribute: '%s'" % attr)

        if attr in self.concrete.keys():
            return self.concrete[attr]

        try:
            val = self.lazies[attr]
        except KeyError:
            raise AttributeError("Invalid attribute: '%s'" % attr)

        if callable(val):
            val = val()

        self.concrete[attr] = val
        return val
