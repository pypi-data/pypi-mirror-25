# -*- coding: utf-8 -*-
import six
from django.apps import AppConfig as DjangoAppConfig

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from modelchemy.v2 import ssot
from collections import defaultdict
from modelchemy.v2.structures.modeling import WorkspaceRegistry
from sqlalchemy.orm import configure_mappers
from sqlalchemy.engine.url import make_url
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import ArgumentError
from django.apps import apps
from modelchemy.v2 import REQUEST_KEY
from modelchemy.v2.shims import import_module


class AppConfig(DjangoAppConfig):
    name = 'modelchemy'
    verbose_name = 'Modelchemy'

    def get_str_from_config_or_default(self, db, config, key, fallback):
        if key not in config:
            return fallback

        candidate = config[key]
        if not isinstance(candidate, six.string_types):
            raise ImproperlyConfigured(
                '\'MODELCHEMY_DATABASES\'[\'%s\'][\'%s\'] is not a valid'
                'string.' % (
                    db, key
                )
            )

        return candidate

    def get_ws_alias_url_tuple(self, definitions):
        result = defaultdict(lambda: defaultdict(lambda: None))

        for k, config in six.iteritems(definitions):
            ws_id = self.get_str_from_config_or_default(k, config,
                                                        'WORKSPACE', 'default')

            alias_id = self.get_str_from_config_or_default(k, config,
                                                           'ALIAS', k)

            if 'URL' not in config:
                raise ImproperlyConfigured(
                    '\'MODELCHEMY_DATABASES\'[\'%s\'][\'URL\'] '
                    'is not present' % (
                        k,
                    )
                )

            try:
                url = make_url(config['URL'])
            except ArgumentError:
                raise ImproperlyConfigured(
                    '\'MODELCHEMY_DATABASES\'[\'%s\'][\'URL\'] '
                    'value is invalid' % (
                        k,
                    )
                )

            result[ws_id][alias_id] = url

        for wk, wv in six.iteritems(result):
            for ak, av in six.iteritems(wv):
                if av is None:
                    raise ImproperlyConfigured(
                        '\'MODELCHEMY_DATABASES\'@\'%s\'@\'%s\' resulted '
                        'in \'None\' url' % (
                            wk, ak,
                        )
                    )
                if not isinstance(av, URL):
                    raise ImproperlyConfigured(
                        '\'MODELCHEMY_DATABASES\'@\'%s\'@\'%s\' resulted '
                        'in something that is not a \'URL\'' % (
                            wk, ak,
                        )
                    )

        return result

    def verify_databases_key_integrity(self, definitions):
        for k, config in six.iteritems(definitions):
            if not isinstance(k, six.string_types):
                raise ImproperlyConfigured(
                    '\'MODELCHEMY_DATABASES\' key \'%s\' is not string' % (
                        k,
                    )
                )

            if (not k.isidentifier()
                or not k.islower()
                or ' ' in k
                or len(k) <= 1
                or k == 'schema'):
                raise ImproperlyConfigured(
                    '\'MODELCHEMY_DATABASES\' key \'%s\' doesn\'t '
                    'comply to naming conventions. '
                    'It must be a valid identifier. '
                    'All characters must be lowercase. '
                    'It musn\'t include \' \' [space] character. '
                    'It musn\'t be equal to \'schema\'' % (
                        k,
                    )
                )

            if not isinstance(config, dict):
                raise ImproperlyConfigured(
                    '\'MODELCHEMY_DATABASES\'[\'%s\'] is not a dict' % (
                        k,
                    )
                )

    def verify_child_configs_integrity(self, definitions):
        for key, config in six.iteritems(definitions):
            if 'URL' not in config:
                raise ImproperlyConfigured(
                    '\'MODELCHEMY_DATABASES\' key \'%s\' doesn\'t '
                    'include a URL parameter.'
                )

            url_candidate = config['URL']

            if not isinstance(url_candidate, six.string_types):
                raise ImproperlyConfigured(
                    '\'MODELCHEMY_DATABASES\'[\'%s\'][\'URL\'] is not a '
                    'string' % (
                        key,
                    )
                )

            if 'WORKSPACE' in config:
                ws_candidate = config['WORKSPACE']

                if not isinstance(ws_candidate, six.string_types):
                    raise ImproperlyConfigured(
                        '\'MODELCHEMY_DATABASES\'[\'%s\'][\'WORKSPACE\'] is '
                        'not a string.' % (
                            key,
                        )
                    )

                if (not ws_candidate.isidentifier()
                    or not ws_candidate.islower()
                    or ' ' in ws_candidate
                    or len(ws_candidate) <= 1
                    or ws_candidate == 'schema'):
                    raise ImproperlyConfigured(
                        '\'MODELCHEMY_DATABASES\'[\'%s\']'
                        '[\'%s\'] doesn\'t '
                        'comply to naming conventions. '
                        'It must be a valid identifier. '
                        'All characters must be lowercase. '
                        'It musn\'t include \' \' [space] character. '
                        'It musn\'t be equal to \'schema\'' % (
                            key,
                            ws_candidate
                        )
                    )

            if 'ALIAS' in config:
                alias_candidate = config['ALIAS']

                if not isinstance(alias_candidate, six.string_types):
                    raise ImproperlyConfigured(
                        '\'MODELCHEMY_DATABASES\'[\'%s\'][\'ALIAS\'] is '
                        'not a string.' % (
                            key,
                        )
                    )

                if (not alias_candidate.isidentifier()
                    or not alias_candidate.islower()
                    or ' ' in alias_candidate
                    or len(alias_candidate) <= 1
                    or alias_candidate == 'schema'):
                    raise ImproperlyConfigured(
                        '\'MODELCHEMY_DATABASES\'[\'%s\']'
                        '[\'%s\'] doesn\'t '
                        'comply to naming conventions. '
                        'It must be a valid identifier. '
                        'All characters must be lowercase. '
                        'It musn\'t include \' \' [space] character.' % (
                            key,
                            alias_candidate,
                        )
                    )

    def ready(self):

        if not hasattr(settings, 'MODELCHEMY_DATABASES'):
            return

        self.verify_databases_key_integrity(settings.MODELCHEMY_DATABASES)
        self.verify_child_configs_integrity(settings.MODELCHEMY_DATABASES)

        ws_alias_url_dict = self.get_ws_alias_url_tuple(
            settings.MODELCHEMY_DATABASES)

        assert isinstance(ws_alias_url_dict, dict), ('\'ws_alias_url_dict\' '
                                                     'is not a dict')

        setattr(ssot, 'workspaces', WorkspaceRegistry(ws_alias_url_dict))

        prefixes = []

        for app_config in apps.get_app_configs():
            for wsk, wsv in six.iteritems(ws_alias_url_dict):
                prefixes.append(
                    (
                        app_config.name,
                        '.%s.%s.%s' % (
                            REQUEST_KEY,
                            wsk,
                            'schema',
                        ),
                    )
                )
                for ak, av in six.iteritems(wsv):
                    prefixes.append(
                        (
                            app_config.name,
                            '.%s.%s.%s.%s' % (
                                REQUEST_KEY,
                                wsk,
                                ak,
                                'schema',
                            ),
                        )
                    )

        for module_name, sub_module in prefixes:
            try:
                import_module(
                    sub_module,
                    module_name
                )
            except ImportError:
                continue

        configure_mappers()

        super(AppConfig, self).ready()
