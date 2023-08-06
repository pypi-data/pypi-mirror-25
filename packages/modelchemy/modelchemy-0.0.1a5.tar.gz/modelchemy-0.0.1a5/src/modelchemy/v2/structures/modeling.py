# -*- coding: utf-8 -*-
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
import six
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import mapper
from sqlalchemy import util
from collections import OrderedDict

from sqlalchemy.ext.declarative.base import _as_declarative
from sqlalchemy.ext.declarative.base import _add_attribute


class DatabaseRegistry(object):
    def __init__(self, url):
        assert isinstance(url, URL), (
            '\'url\' param should be a sqlalchemy URL')

        self._factories = {}
        self._memoized = {}

        self._factories.update({
            'Engine': self.generate_engine(url),
            'MetaData': self.generate_metadata,
            'Base': self.generate_base,
            'Session': self.generate_session,
        })

    @property
    def keys(self):
        return self._factories.keys()

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

    def generate_engine(self, url):
        def factory():
            return create_engine(url)

        return factory

    def generate_metadata(self):
        metadata = MetaData()
        metadata.bind = self.Engine
        return metadata

    def generate_base(self):
        return declarative_base(metadata=self.MetaData)

    def generate_session(self):
        Session = sessionmaker()
        Session.configure(bind=self.Engine)
        return Session


class AliasAccessor(object):
    def __init__(self, key, child):
        self._key = key
        self._child = child

    def __getattr__(self, item):
        return self.get(item)

    def __getitem__(self, item):
        return self.get(item)

    def get(self, key):
        return self.storage_get(key)

    def storage_get(self, key):
        assert isinstance(key, six.string_types), (
            'key must be a valid string' % (

            )
        )

        if len(key) <= 2:
            raise AttributeError("Invalid attribute: '%s'" % key)

        f_char = key[0]

        if f_char.isupper():
            if key not in ['Table', 'Base',
                           'MetaData', 'Engine',
                           'Session']:
                raise AttributeError("Invalid attribute: '%s'" % key)

            if key == 'Table':
                return WorkspaceTable(self, self._key)
            elif key == 'Base':
                return self._child.Base
            elif key == 'Engine':
                return self._child.Engine
            elif key == 'MetaData':
                return self._child.MetaData
            elif key == 'Session':
                return self._child.Session
        else:
            if key not in self._child.keys:
                raise AttributeError("Invalid attribute: '%s'" % key)

            try:
                val = getattr(self._child, key)
            except KeyError:
                raise AttributeError("Invalid attribute: '%s'" % key)

            return val

        raise AttributeError("Invalid attribute: '%s'" % key)


class AliasRegistry(object):
    def __init__(self, elements):
        self._registry = {}

        assert isinstance(elements, dict), (
            '\'elements\' param should be a dict')

        for ak, av in six.iteritems(elements):
            self._registry[ak] = AliasAccessor(ak, DatabaseRegistry(av))

    @property
    def registry(self):
        return self._registry

    @property
    def keys(self):
        return self.registry.keys()

    def __getattr__(self, item):
        return self.get(item)

    def __getitem__(self, item):
        return self.get(item)

    def get(self, key):
        return self.storage_get(key)

    def storage_get(self, key):
        if key not in self.registry.keys():
            raise AttributeError("Invalid attribute: '%s'" % key)

        try:
            val = self.registry[key]
        except KeyError:
            raise AttributeError("Invalid attribute: '%s'" % key)

        return val


class WorkspaceTableType(type):
    def __new__(cls, name, bases, dct):
        return type.__new__(cls, name, bases, dct)


class WorkspaceMapperType(type):
    def __new__(cls, name, bases, dct):
        return type.__new__(cls, name, bases, dct)


class BaseWorkspaceTable(object, six.with_metaclass(WorkspaceTableType)):
    def __init__(self, accessor, ws, name, metadata, *args, **kwargs):
        self._accessor = accessor
        self._ws = ws
        self._name = name
        self._metadata = metadata
        self._max = len(self._metadata)
        self._enum = enumerate(self._metadata)

        self._table = Table(
            self._name,
            self._accessor.MetaData,
            *args,
            **kwargs,
        )

        tables = OrderedDict()
        for m in metadata:
            alias_accessor = getattr(self._accessor, m)
            tables[m] = self._table.tometadata(alias_accessor.MetaData)

        self._tables = tables

    def __iter__(self):
        return six.iteritems(self._tables)

    def __len__(self):
        return len(self._tables)

    @property
    def ts(self):
        return self.__iter__()

    @property
    def tables(self):
        return self.ts

    @property
    def t(self):
        return self._table

    @property
    def table(self):
        return self.t

    def __getitem__(self, item):
        assert isinstance(item, six.string_types), (
            'key must be a valid string' % (

            )
        )

        if item not in self._tables:
            raise IndexError(
                'Item with index \'%s\' doesn\'t exist.' % (item,)
            )

        return self._tables[item]


class ExposeDict(object):
    def __init__(self, dict_):
        self._dict = dict_

    def __iter__(self):
        return six.iteritems(self._dict)

    def __getitem__(self, item):
        assert isinstance(item, six.string_types), (
            'key must be a valid string' % (

            )
        )

        if item not in self._dict:
            raise IndexError(
                'Item with index \'%s\' doesn\'t exist.' % (item,)
            )

        return self._dict[item]

    def __contains__(self, item):
        return item in self._dict


class BaseWorkspaceMapper(object, six.with_metaclass(WorkspaceMapperType)):
    def __init__(self, accessor, ws, class_, tables, *args, **kwargs):
        self._accessor = accessor
        self._ws = ws
        self._class = class_

        self._mapper = mapper(
            class_,
            tables.table,
            *args,
            **kwargs
        )

    def __call__(self, *args, **kwargs):
        return self._mapper


class FluentSyntaxBase(object):
    _inclusion = []
    _exclusion = []
    _table = None

    def __init__(self, table, inc, exc):
        self._table = table
        self._inclusion = inc
        self._exclusion = exc

    def __call__(self, *args, **kwargs):

        inc_set = set(self._table.keys).intersection(set(self._inclusion))
        exc_set = set(inc_set).difference(set(self._exclusion))
        in_ = list(exc_set)

        kwargs['__modelchemy_alias_list'] = in_
        return self._table(*args, **kwargs)

    def __update_collection(self, collection, alias):
        if isinstance(alias, six.string_types):
            collection.append(alias)

        if isinstance(alias, (list, tuple)):
            collection.extend(alias)

    def _update_exclusion(self, alias):
        self.__update_collection(self._exclusion, alias)

    def _update_inclusion(self, alias):
        self.__update_collection(self._inclusion, alias)


class WorkspaceTableAttachIntoFluentSyntax(FluentSyntaxBase):
    def and_(self, alias):
        self._update_inclusion(alias)
        return self

    @property
    def detach(self):
        return WorkspaceTableDetachFluentSyntax(self._table,
                                                self._inclusion,
                                                self._exclusion)


class WorkspaceTableDetachIntoFluentSyntax(FluentSyntaxBase):
    def and_(self, *args):
        self._update_exclusion(args)
        return self

    @property
    def attach(self):
        return WorkspaceTableAttachFluentSyntax(self._table,
                                                self._inclusion,
                                                self._exclusion)


class WorkspaceTableAttachFluentSyntax(FluentSyntaxBase):
    def to(self, *args):
        self._update_inclusion(args)
        return WorkspaceTableAttachIntoFluentSyntax(self._table,
                                                    self._inclusion,
                                                    self._exclusion)


class WorkspaceTableDetachFluentSyntax(FluentSyntaxBase):
    def from_(self, *args):
        self._update_exclusion(args)
        return WorkspaceTableDetachIntoFluentSyntax(self._table,
                                                    self._inclusion,
                                                    self._exclusion)


class WorkspaceTable(object):
    def __init__(self, accessor, ws):
        self._accessor = accessor
        self._ws = ws

    @property
    def keys(self):
        return self._accessor.all

    @property
    def attach(self):
        return WorkspaceTableAttachFluentSyntax(self, [], [])

    @property
    def detach(self):
        base = [k for k in self.keys]
        return WorkspaceTableDetachFluentSyntax(self, base, [])

    def __call__(self, *args, **kwargs):

        try:
            name, args = args[0], args[1:]
        except IndexError:
            raise TypeError("Table() takes at least one arguments")

        if not isinstance(name, six.string_types):
            raise TypeError("Table() first argument must be a table name")

        into = kwargs.pop('__modelchemy_alias_list', self._accessor.all)

        return (
            type('WorkspaceTable',
                 (BaseWorkspaceTable,),
                 {})(self._accessor, self._ws,
                     name, into, *args, **kwargs))


class WorkspaceMapper(object):
    def __init__(self, accessor, ws):
        self._accessor = accessor
        self._ws = ws

    def __call__(self, *args, **kwargs):
        try:
            class_, tables, args = args[0], args[1], args[2:]
        except IndexError:
            raise TypeError("Table() takes at least two arguments")

        util.assert_arg_type(class_, type, 'class_')

        util.assert_arg_type(tables, BaseWorkspaceTable, 'tables')

        return (
            type('WorkspaceMapper', (BaseWorkspaceMapper,), {})(
                self._accessor, self._ws, class_, tables, *args, **kwargs
            )
        )


class WorkspaceBase(object):
    def __init__(self, accessor, ws):
        self._accessor = accessor
        self._ws = ws
        self._base = declarative_base(
            metadata=self._accessor.MetaData,
            metaclass=MyDeclarativeMeta,
        )
        setattr(self._base, '__ws_accessor__', self._accessor)

    def __call__(self, *args, **kwargs):
        return self._base


def convert_to_set_list(candidate):
    if isinstance(candidate, six.string_types):
        return (candidate,)
    if isinstance(candidate, (list, tuple)):
        return list(set(candidate))

    return None


def get_base_get_alias_list(cls, all):
    keys_set = set(all)
    keys_list = list(keys_set)

    alias_list = getattr(cls, '__aliases__', keys_list)
    alias_exclude_list = getattr(cls, '__aliases_exclude__', [])

    alias_list = convert_to_set_list(alias_list)

    if not alias_list:
        alias_list = []

    alias_exclude_list = convert_to_set_list(alias_exclude_list)
    if not alias_exclude_list:
        alias_exclude_list = []

    inclusion_list = list(keys_set.intersection(set(alias_list)))

    return list(
        set(inclusion_list).difference(set(alias_exclude_list)))


class MyDeclarativeMeta(type):
    def __init__(cls, classname, bases, dict_):
        if '_decl_class_registry' not in cls.__dict__:
            _as_declarative(cls, classname, cls.__dict__)

            # Work to apply to all databases
            ws_accessor = getattr(cls, '__ws_accessor__')
            alias_list = get_base_get_alias_list(cls, ws_accessor.all)
            table = cls.__table__

            for m in alias_list:
                table.tometadata(getattr(ws_accessor, m).MetaData)

        type.__init__(cls, classname, bases, dict_)

    def __setattr__(cls, key, value):
        _add_attribute(cls, key, value)


class WorkspaceAccessor(object):
    def __init__(self, key, child):
        self._key = key
        self._child = child

        self._raw_metadata_memo = None

    @property
    def raw_metadata(self):
        if self._raw_metadata_memo is None:
            self._raw_metadata_memo = MetaData()
        return self._raw_metadata_memo

    @property
    def all(self):
        return self._child.keys

    def __getattr__(self, item):
        return self.get(item)

    def __getitem__(self, item):
        return self.get(item)

    def get(self, key):
        return self.storage_get(key)

    def storage_get(self, key):
        assert isinstance(key, six.string_types), (
            'key must be a valid string' % (

            )
        )

        if len(key) <= 2:
            raise AttributeError("Invalid attribute: '%s'" % key)

        f_char = key[0]

        if f_char.isupper():
            if key not in ['Table', 'Mapper', 'Base', 'MetaData']:
                raise AttributeError("Invalid attribute: '%s'" % key)

            # ToDo: Change to memoized version of files

            if key == 'MetaData':
                return self.raw_metadata
            if key == 'Base':
                factory = WorkspaceBase(self, self._key)
                return factory()
            elif key == 'Table':
                return WorkspaceTable(self, self._key)
            elif key == 'Mapper':
                return WorkspaceMapper(self, self._key)
        else:
            if key not in self._child.keys:
                raise AttributeError("Invalid attribute: '%s'" % key)

            try:
                val = getattr(self._child, key)
            except KeyError:
                raise AttributeError("Invalid attribute: '%s'" % key)

            return val

        raise AttributeError("Invalid attribute: '%s'" % key)


class WorkspaceRegistry(object):
    def __init__(self, elements):
        self._registry = {}

        assert isinstance(elements, dict), (
            '\'elements\' param should be a dict')

        for wk, wv in six.iteritems(elements):
            self._registry[wk] = WorkspaceAccessor(wk, AliasRegistry(wv))

    @property
    def registry(self):
        return self._registry

    @property
    def keys(self):
        return self.registry.keys()

    def __getattr__(self, item):
        return self.get(item)

    def __getitem__(self, item):
        return self.get(item)

    def get(self, key):
        return self.storage_get(key)

    def storage_get(self, key):

        assert isinstance(key, six.string_types), (
            'key must be a valid string' % (

            )
        )

        if len(key) <= 2:
            raise AttributeError("Invalid attribute: '%s'" % key)

        if key not in self.registry.keys():
            raise AttributeError("Invalid attribute: '%s'" % key)

        try:
            val = self.registry[key]
        except KeyError:
            raise AttributeError("Invalid attribute: '%s'" % key)

        return val
