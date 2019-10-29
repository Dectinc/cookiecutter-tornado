#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 eVision.ai Inc. All Rights Reserved.

import os
from configparser import ConfigParser

from evision.lib.config import ConfigSection, EvisionConfig
from evision.lib.log import logutil

from {{ cookiecutter.project_slug }}.util import paths

logger = logutil.get_logger()

class {{ cookiecutter.project_slug|title }}Config(EvisionConfig):
    __default_config = paths.config_path('.last.ini')

    def __init__(self, default_file=None, load_default=False):
        self._default_config = default_file if default_file else self.__default_config

        EvisionConfig.__init__(self, load_default)

    @property
    def recover_file(self):
        return self._default_config

    @recover_file.setter
    def recover_file(self, recover_path):
        self._default_config = recover_path

    def load_last_or_by_profile(self, profile=None):
        if os.path.exists(self.recover_file) and os.path.isfile(self.recover_file):
            last_cfg = ConfigParser()
            last_cfg.read(self.recover_file, encoding='utf-8')

            if last_cfg.has_option(ConfigSection.TORNADO, 'profile') \
                and last_cfg.get(ConfigSection.TORNADO, 'profile') == profile:
                self.load(self.__default_config)
                return True

        logger.info('Profile changed, reloading configurations...')
        self.load_default()
        _profile_conf = paths.config_path('{}.ini'.format(profile))
        if os.path.exists(_profile_conf):
            self.load(_profile_conf)
        self.save()
