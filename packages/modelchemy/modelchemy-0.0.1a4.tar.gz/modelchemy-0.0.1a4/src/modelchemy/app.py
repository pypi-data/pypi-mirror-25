# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

import six
from django.apps import AppConfig as DjangoAppConfig
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from modelchemy import REQUEST_KEY
from modelchemy import SiteDatabaseRecordFactory
from modelchemy import dbs
from modelchemy.shims import import_module

from sqlalchemy.orm import configure_mappers


class AppConfig(DjangoAppConfig):
    name = 'modelchemy'
    verbose_name = 'Modelchemy'

    def ready(self):
        for key, config in six.iteritems(settings.MODELCHEMY_DATABASES):
            if "URL" not in config:
                raise ImproperlyConfigured(
                    "The database '%s' doesn't include a URL config." % (
                        key
                    )
                )

            alias = key if "ALIAS" not in config else config["ALIAS"]

            dbs.set(alias, SiteDatabaseRecordFactory(config['URL']))

            for app_config in apps.get_app_configs():

                try:
                    import_module(".%s.%s" % (
                        REQUEST_KEY,
                        alias),
                                  app_config.name)
                except ImportError:
                    continue

        configure_mappers()
        super(AppConfig, self).ready()
