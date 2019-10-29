# -*- coding: utf-8 -*-

"""Global settings for the project"""

import logging
import os
from os import path as osp

import tornado.template
from tornado.options import define, options

from evision.lib.config import ConfigSection
from evision.lib.constant import DeploymentType, Keys
from evision.lib.log import logconfig, logutil
from evision.lib.util import PathUtil

from {{cookiecutter.project_slug}}.util import paths
from {{cookiecutter.project_slug}}.util.config import {{ cookiecutter.project_slug|title }}Config

logger = logutil.get_logger()

# ##################################################################
# path initialization
__ROOT = osp.abspath(osp.dirname(osp.abspath(__file__)))
PathUtil.add_path(__ROOT)
__BASE_PACKAGE__ = '{{ cookiecutter.project_slug }}'

# ##################################################################
# parse command line arguments
define('port', default=None, help='run on the given port', type=int)
define('config', default=None, help='tornado config file')
define('debug', default=True, help='debug mode')
define('profile', default=DeploymentType.DEV, help='deployment profile')
define('auto_starting', default=False, help='auto starting service')
define('log', default='warn', help='logging level')

options.parse_command_line()

# ##################################################################
# Deployment Configuration
CONFIG = {{ cookiecutter.project_slug|title }}Config()
if options.profile:
    _PROFILE = options.profile.lower()
elif 'DEPLOYMENT_TYPE' in os.environ:
    _PROFILE = os.environ['DEPLOYMENT_TYPE'].lower()
else:
    _PROFILE = DeploymentType.PROD
# 读取部署profile相关的配置
CONFIG.load_last_or_by_profile(_PROFILE)
# extra config
if options.config and osp.exists(options.config):
    CONFIG.load(options.config)
CONFIG.read_dict({ConfigSection.TORNADO: {k: str(v) for k, v in options.items()}})
logging.info('Configurations: \n{}'.format(CONFIG))

if not options.port:
    options.port = CONFIG.getint('project', 'port')

__debug_mode = _PROFILE != DeploymentType.PROD and options.debug
APP_SETTINGS = {
    'debug': __debug_mode,
    'static_path': paths.media_path(),
    'static_url_prefix': paths.STATIC_URL_PREFIX,
    'static_hash_cache': not __debug_mode,
    'serve_traceback': __debug_mode,
    'cookie_secret': 'chenshijiang@evision.ai',
    'xsrf_cookies': False,
    'template_loader': tornado.template.Loader(paths.TEMPLATE_ROOT),
    Keys.AUTO_STARTING: options.auto_starting
}
logger.info('Extra settings: ' + ''.join(
    ['\n{}={}'.format(k, v) for k, v in sorted(APP_SETTINGS.items())]))

# ##################################################################
# logger config
LOG_LEVEL = logging.DEBUG if __debug_mode else options.logging
log_dir = paths.log_path(CONFIG.get(ConfigSection.PROJECT, 'log_dir'))
logconfig.config(options.port, {}, log_level=LOG_LEVEL, show_console=_PROFILE == DeploymentType.DEV)

__all__ = [
    'APP_SETTINGS',
    'CONFIG',
]
