# -*- coding: UTF-8 -*-
from modelchemy.settings import modelchemy_settings

def default_shard_chooser(mapper, instance, clause=None):
    return modelchemy_settings.DEFAULT_SHARD

def default_id_chooser(query, ident):
    return [modelchemy_settings.DEFAULT_SHARD, ]

def default_query_chooser(query):
    return [modelchemy_settings.DEFAULT_SHARD, ]