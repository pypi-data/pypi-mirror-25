# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy import util
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session


class SiteDatabaseRecordFactory(object):
    @property
    def factories(self):
        return self._factories

    @property
    def memoized(self):
        return self._memoized

    def __getattr__(self, attr):
        return self.__storage_get(attr)

    def __getitem__(self, item):
        return self.__storage_get(item)

    def __storage_get(self, key):
        if key not in self.factories.keys():
            raise AttributeError("Invalid attribute: '%s'" % key)

        if key in self.memoized.keys():
            return self.memoized[key]

        try:
            val = self.factories[key]
        except KeyError:
            raise AttributeError("Invalid attribute: '%s'" % key)

        if callable(val):
            val = val()

        self.memoized[key] = val
        return val

    def generate_metadata(self):
        metadata = MetaData()
        metadata.bind = self.engine
        return metadata

    def generate_base(self):
        return declarative_base(metadata=self.metadata)

    def generate_session(self):
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        return Session

    def generate_engine(self, url):
        def factory():
            return create_engine(url)

        return factory

    def __init__(self, url):
        self._factories = {}
        self._memoized = {}

        self.factories.update({
            'engine': self.generate_engine(url),
            'metadata': self.generate_metadata,
            'base': self.generate_base,
            'Session': self.generate_session,
        })


class ShardedQuery(Query):
    def __init__(self, *args, **kwargs):
        super(ShardedQuery, self).__init__(*args, **kwargs)
        self.id_chooser = self.session.id_chooser
        self.query_chooser = self.session.query_chooser
        self._shard_id = None

    def set_shard(self, shard_id):
        """return a new query, limited to a single shard ID.
        all subsequent operations with the returned query will
        be against the single shard regardless of other state.
        """

        q = self._clone()
        q._shard_id = shard_id
        return q

    def _execute_and_instances(self, context):
        def iter_for_shard(shard_id):
            context.attributes['shard_id'] = shard_id
            result = self._connection_from_session(
                mapper=self._mapper_zero(),
                shard_id=shard_id).execute(
                context.statement,
                self._params)
            return self.instances(result, context)

        if self._shard_id is not None:
            return iter_for_shard(self._shard_id)
        else:
            partial = []
            for shard_id in self.query_chooser(self):
                partial.extend(iter_for_shard(shard_id))

            # if some kind of in memory 'sorting'
            # were done, this is where it would happen
            return iter(partial)

    def get(self, ident, **kwargs):
        if self._shard_id is not None:
            return super(ShardedQuery, self).get(ident)
        else:
            ident = util.to_list(ident)
            for shard_id in self.id_chooser(self, ident):
                o = self.set_shard(shard_id).get(ident, **kwargs)
                if o is not None:
                    return o
            else:
                return None


class RoutedSession(Session):
    def __init__(self, registry, query_cls=ShardedQuery, **kwargs):
        """Construct a ShardedSession.
        :param shard_chooser: A callable which, passed a Mapper, a mapped
          instance, and possibly a SQL clause, returns a shard ID.  This id
          may be based off of the attributes present within the object, or on
          some round-robin scheme. If the scheme is based on a selection, it
          should set whatever state on the instance to mark it in the future as
          participating in that shard.
        :param id_chooser: A callable, passed a query and a tuple of identity
          values, which should return a list of shard ids where the ID might
          reside.  The databases will be queried in the order of this listing.
        :param query_chooser: For a given Query, returns the list of shard_ids
          where the query should be issued.  Results from all shards returned
          will be combined together into a single listing.
        :param shards: A dictionary of string shard names
          to :class:`~sqlalchemy.engine.Engine` objects.
        """
        super(RoutedSession, self).__init__(query_cls=query_cls, **kwargs)
        from modelchemy.settings import modelchemy_settings

        self.shard_chooser = modelchemy_settings.SHARD_CHOOSER
        self.id_chooser = modelchemy_settings.ID_CHOOSER
        self.query_chooser = modelchemy_settings.QUERY_CHOOSER
        self.registry = registry
        self.__binds = {}
        self.__using = None
        for k in self.registry.keys:
            self.bind_db(k, self.registry[k].engine)

        self.connection_callable = self.connection

    @property
    def using(self):
        return self.__using

    @using.setter
    def using(self, db):
        self.__using = db

    def connection(self, mapper=None, instance=None, db=None, **kwargs):

        if self.__using is not None:
            db = self.__using

            if self.transaction is not None:
                return self.transaction.connection(mapper, db=db)
            else:
                return self.get_bind(
                    mapper,
                    db=db,
                    instance=instance
                ).contextual_connect(**kwargs)

        if db is None:
            db = self.shard_chooser(mapper, instance)

        if self.transaction is not None:
            return self.transaction.connection(mapper, db=db)
        else:
            return self.get_bind(
                mapper,
                db=db,
                instance=instance
            ).contextual_connect(**kwargs)

    def get_bind(self, mapper, db=None, instance=None, clause=None, **kw):

        if self.__using is not None:
            return self.__binds[self.__binds]

        if db is None:
            db = self.shard_chooser(mapper, instance, clause=clause)
        return self.__binds[db]

    def bind_db(self, shard_id, bind):
        self.__binds[shard_id] = bind

    def close(self):
        super(RoutedSession, self).close()


class BaseRoot(object):
    def __init__(self):
        self.metadata = MetaData()
        self.base = declarative_base(metadata=self.metadata)


class SiteDatabasesRegistry(object):
    def __init__(self):
        self._registry = {}
        self.base = BaseRoot()
        self.Session = sessionmaker(class_=RoutedSession, registry=self)

    def __getattr__(self, key):
        return self.get(key)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    @property
    def registry(self):
        return self._registry

    @property
    def keys(self):
        return self.registry.keys()

    def get(self, key):
        return self.storage_get(key)

    def set(self, key, value):
        self.__storage_set(key, value)

    def storage_get(self, key):
        if key not in self.registry.keys():
            raise AttributeError("Invalid attribute: '%s'" % key)

        try:
            val = self.registry[key]
        except KeyError:
            raise AttributeError("Invalid attribute: '%s'" % key)

        return val

    def __storage_set(self, key, value):

        if not isinstance(value, SiteDatabaseRecordFactory):
            raise AttributeError("Invalid value for key: '%s'" % key)

        self.registry[key] = value


dbs = SiteDatabasesRegistry()
