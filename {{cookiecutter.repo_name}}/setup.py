#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from glob import glob
import os.path
from os.path import basename, splitext

from setuptools import find_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def _read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def _read_as_list(fname):
    content = _read(fname)
    return [_.strip() for _ in content.split('\n') if _ and _.strip()]


setup(
    name='{{ cookiecutter.project_name }}',
    version='{{ cookiecutter.version }}',
    license='GPLv3',
    description='{{ cookiecutter.description }}',
    long_description=_read('README.md'),
    author='{{ cookiecutter.author_name }}',
    author_email='{{ cookiecutter.email }}',
    url='https://{{ cookiecutter.repo_hosting_domain }}/{{ cookiecutter.repo_username }}/{{ cookiecutter.repo_name }}',
    include_package_data=True,
    packages=find_packages('{{ cookiecutter.project_slug }}', exclude=['*.pyc', ]),
    package_data={
        '': glob('data/config/*.ini'),
    },
    py_modules=[splitext(basename(path))[0] for path in glob('{{ cookiecutter.project_slug }}/*.py')],
    zip_safe=False,
    test_suite='tests',
    setup_requires=['pytest-runner'],
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    project_urls={
        'Issue Tracker': 'https://{{ cookiecutter.repo_hosting_domain }}/{{ cookiecutter.repo_username }}/{{ cookiecutter.repo_name }}/issues',
    },
    keywords=[
        '{{ cookiecutter.project_slug }}', 'tornado'
    ],
    install_requires=_read_as_list('requirements/base.txt'),
    tests_require=_read_as_list('requirements/test.txt'),
    entry_points={

    }
)
