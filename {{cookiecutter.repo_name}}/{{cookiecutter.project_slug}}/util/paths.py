#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Store all preset paths
#
# @version: {{ cookiecutter.version }}
#
import os
import os.path
from functools import partial
from os.path import join as pjoin

ROOT_DIR = os.path.abspath(pjoin(os.path.dirname(__file__), '..', '..'))


def __path(*sub_dirs):
    sub_dirs = [_ for _ in sub_dirs if _ is not None]
    return os.path.abspath(os.path.join(ROOT_DIR, *sub_dirs))


STATIC_URL_PREFIX = '/{{ cookiecutter.project_slug }}/v1/'
SOURCE_ROOT = __path('{{ cookiecutter.project_slug }}')
RESOURCE_ROOT = __path('resources')
TEMPLATE_ROOT = __path('resources', 'templates')
DATA_ROOT = __path('data')
DOC_ROOT = __path('docs')

data_path = partial(__path, 'data')
media_path = partial(data_path, 'media')
model_path = partial(data_path, 'model')
log_path = partial(data_path, 'logs')
config_path = partial(data_path, 'config')
template_path = partial(__path, 'resources', 'templates')

for _path in [media_path(), model_path(),
              log_path(), config_path(),
              RESOURCE_ROOT, TEMPLATE_ROOT]:
    if not os.path.exists(_path):
        os.makedirs(_path)

DEFAULT_CONFIG_FILE = config_path('default.ini')
