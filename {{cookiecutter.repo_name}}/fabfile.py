#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import sys

from fabric import task

sys.path.insert(0, os.getcwd())

CMD_PYLINT = 'pylint'


@task
def clean():
    """Remove temporary files."""
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith('.pyc') or name.endswith('~'):
                os.remove(os.path.join(root, name))


@task
def devserve(port=8888, logging='debug', debug=True):
    """Start the server in development mode."""
    os.system(f'python run.py --port={port} --logging={logging}, debug={debug}')


@task
def serve(port=8888, logging='warn', debug=False):
    os.system(f'python run.py --port={port} --logging={logging}, debug={debug}')


@task
def mo():
    pass


@task
def po():
    pass
