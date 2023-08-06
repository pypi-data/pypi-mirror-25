# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import os


def load_model_apps(base, route):

    result = []

    for dirname, dirnames, files in os.walk(route):

        if len(dirnames) == 0: continue

        for sub in dirnames:
            if sub == 'modelchemy':
                if '__init__.py' not in files: continue

                result.append(
                    dirname[len(base, ) + 1:].replace(os.path.sep, '.'))

    return result