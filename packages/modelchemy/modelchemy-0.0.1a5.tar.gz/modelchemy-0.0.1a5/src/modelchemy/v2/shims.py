# -*- coding: utf-8 -*-

try:
    from importlib import import_module
except ImportError:
    from django.utils.module_loading import import_module