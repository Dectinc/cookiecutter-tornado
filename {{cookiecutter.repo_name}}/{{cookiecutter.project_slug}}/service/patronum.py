#! /usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
import hashlib
import json
from operator import itemgetter
import time
import uuid

from evision.lib.config import ConfigSection
from evision.lib.log import logutil
from evision.lib.mixin import FailureCountMixin
from evision.lib.util import CacheUtil
import requests
from settings import CONFIG

from {{cookiecutter.project_slug}}.util.constant import Keys, Error

logger = logutil.get_logger()


def get_device_info():
    """Get terminal/device info

    :return: MAC
    """
    return uuid.getnode()


def get_timeout(kwargs, default_=2):
    """从参数中获取timeout值,如果参数中未提供,使用默认值"""
    if kwargs and 'timeout' in kwargs and kwargs['timeout'] > 0:
        timeout = kwargs.pop('timeout')
    else:
        timeout = default_
    return timeout


class PatronumApi(Enum):
    # 注册服务器
    REGISTER = 'register'


class ServerInfoMixin(object):
    """Server信息封装"""

    def __init__(self, **kwargs):
        self.host = None

        self.server_id = None
        self.server_token = None

        # 终端访问广目平台的授权
        self.authorization_key = None
        # 终端对应的APP_ID
        self.app_id = None
        # 终端对应的APP所需的APP_SECRET
        self.app_secret = None

        self._server_info_inited = False
        self.__backup = {}

    def set_host(self, host):
        self.host = host

    def set_app_params(self, authorization_key, app_id, app_secret):
        """设置应用相关信息"""
        self.authorization_key = authorization_key
        self.app_id = app_id
        self.app_secret = str(app_secret)

    def set_server_params(self, server_id, server_token):
        """设置终端相关信息"""
        self.server_id = server_id
        self.server_token = server_token
        self._server_info_inited = True

    @property
    def inited(self):
        return self._server_info_inited

    def __str__(self):
        return json.dumps(self.server_params)

    def info(self):
        return self.server_id, self.server_token

    @property
    def server_params(self):
        """终端相关信息

        说明: NUC之前被当做一种类型的服务器,后来切换为终端.方法名称未更新,请不要被误导
        """
        return {} if not self._server_info_inited else {
            Keys.SERVER_ID: int(self.server_id),
            Keys.SERVER_TOKEN: str(self.server_token)
        }

    @property
    def app_params(self):
        """APP相关信息"""
        return {
            Keys.APP_ID: self.app_id,
            Keys.TIMESTAMP: int(time.time()),
            Keys.NOISE_STR: CacheUtil.random_string()
        }

    def wrap(self, params):
        """ add server id token and app related id and token
        @apiDefine PatronumApiParams

        @apiParam {string} app_id APP ID
        @apiParam {number} server_id 服务器ID
        @apiParam {string} server_token 服务器TOKEN
        @apiParam {number} timestamp 时间戳
        @apiParam {string} noise_str 噪声字符串
        @apiParam {string} sign 根据参数生成的签名
        """
        if not params:
            params = {}
        # 在API调用中添加终端相关信息
        params.update(self.server_params)
        # 在API调用中添加APP相关信息
        params.update(self.app_params)
        params = {key: str(value) for key, value in params.items()
                  if value is not None}

        param_string = '&'.join(
            ['{}={}'.format(key, value)
             for key, value in sorted(params.items(), key=itemgetter(0))])
        params[Keys.SIGN] = \
            hashlib.md5((param_string + self.app_secret).encode()) \
                .hexdigest().upper()
        return params

    def register(self, request_url, authorization_key, app_id, app_token):
        """Get terminal id

        Sample response:
        HTTP/1.1 200 OK
         {
            "code": 0,
            "msg": "ok",
            "data": {
                "server_id": 1,
                "server_token": 'ABCD239438SD9D'
            }
        }

        Get server id with server info or camera info
        :param request_url:
        :param authorization_key: api authorization key
        :param app_id: api related app id
        :param app_token: api related app secret
        :return: server_info
        """
        device_info = get_device_info()
        if isinstance(authorization_key, bytes):
            authorization_key = authorization_key.decode()
        self.set_app_params(authorization_key, app_id, app_token)
        try:
            params = {
                "device_id": device_info,
                "authorization_key": authorization_key
            }
            params = self.wrap(params)
            response = requests.post(request_url, params, timeout=5)
            if response.status_code != 200:
                logger.error('Failed registering device, status={}, url={}, params={}',
                             response.status_code, response.url, params)
                raise Exception('Failed calling url={}'.format(response.url))
            result = response.json()
            if Keys.DATA not in result or result[Keys.CODE] != 0 \
                or result[Keys.DATA] is None:
                logger.warn('Failed getting server id, device_info={}, url={}, '
                            'response={}'.format(device_info, request_url, result))
            response_data = result[Keys.DATA]

            self.set_server_params(response_data[Keys.SERVER_ID],
                                   response_data[Keys.SERVER_TOKEN])
            self.save_config()
        except requests.ReadTimeout as rte:
            logger.error('[Terminal-{}] Failed registering to={}: {}',
                         self.server_id, request_url, rte)
            raise rte
        except ConnectionError as ce:
            logger.error('Url={} is not a valid Patronum registering address',
                         request_url)
            raise ce
        except Exception as e:
            logger.exception('Failed registering server with device_info={}, '
                             'authorization key={}, app[{}]={}: {}',
                             device_info, authorization_key, app_id, app_token, e)
            raise e

    def backup(self):
        """备份服务器配置
        用于在使用新配置注册广目平台失败时回滚"""
        self.__backup = {
            Keys.PATRONUM: self.host,
            Keys.SERVER_ID: int(self.server_id),
            Keys.SERVER_TOKEN: str(self.server_token),
            Keys.AUTHORIZATION: self.authorization_key,
            Keys.APP_ID: self.app_id,
            Keys.APP_SECRET: self.app_secret
        }

    def restore(self):
        """回滚服务器配置信息"""
        if not hasattr(self, '__backup') or not self.__backup:
            return
        self.host = self.__backup[Keys.PATRONUM]
        self.server_id = self.__backup[Keys.SERVER_ID]
        self.server_token = self.__backup[Keys.SERVER_TOKEN]
        self.authorization_key = self.__backup[Keys.AUTHORIZATION]
        self.app_id = self.__backup[Keys.APP_ID]
        self.app_secret = self.__backup[Keys.APP_SECRET]

    def save_config(self):
        CONFIG.update_section(ConfigSection.PATRONUM, {
            'host': self.host,
            'key': self.authorization_key,
            'app_id': self.app_id,
            'app_secret': self.app_secret,
            'server_id': self.server_id,
            'server_token': self.server_token
        })
        CONFIG.save()


class PatronumWrapper(ServerInfoMixin, FailureCountMixin):
    """广目平台API调用封装"""
    _FAIL_COUNT_THRESHOLD = 10
    _fail_count = 0

    def __init__(self):
        FailureCountMixin.__init__(self)
        ServerInfoMixin.__init__(self)
        self.set_host(CONFIG.get('patronum', 'host'))
        self.set_app_params(CONFIG.get('patronum', 'key'),
                            CONFIG.get('patronum', 'app_id'),
                            CONFIG.get('patronum', 'app_secret'))

    def url(self, api):
        """根据API名称获取API调用地址"""
        if not api:
            raise ValueError('Api identifier not provided')
        if isinstance(api, PatronumApi):
            api = api.value
        return 'http://{}{}'.format(self.host, CONFIG.get('patronum_api', api))

    def __make_request(self, method, api, params: dict = None, data: dict = None,
                       **kwargs):
        """向广目平台发送请求"""
        if not self.inited:
            return
        request_url = self.url(api)
        try:
            if method == 'get':
                params = self.wrap(params)
                kwargs.setdefault('allow_redirects', True)
            else:
                data = self.wrap(data)
            result = requests.request(method, request_url,
                                      data=data, params=params,
                                      timeout=get_timeout(kwargs), **kwargs)
            if result is None:
                raise Error.HttpNoResponse()
            elif not result.ok:
                raise Error.HttpInvalidStatus(result.status_code)
            logger.info('[Terminal-{}] Calling api={}: {}',
                        self.server_id, request_url, result.json())
            return result
        except requests.ReadTimeout as rte:
            logger.error('[Terminal-{}] Failed calling api={}: {}',
                         self.server_id, request_url, rte)
        except Exception as e:
            logger.exception('[Terminal-{}] Failed calling api={}: {}',
                             self.server_id, request_url, e)
        self.accumulate_failure_count()

    def __make_get(self, api, params: dict = None, **kwargs):
        return self.__make_request('get', api, params=params, **kwargs)

    def __make_post(self, api, params: dict = None, **kwargs):
        return self.__make_request('post', api, data=params, **kwargs)

    def __register_server(self):
        """在广目平台注册本终端

        说明: NUC之前被当做一种类型的服务器,后来切换为终端.方法名称未更新,请不要被误导
        """
        request_url = self.url(PatronumApi.REGISTER)

        try:
            self.register(request_url, self.authorization_key,
                          self.app_id, self.app_secret)
            self.reset_failure_count()
            return True
        except Exception as e:
            logger.error('Failed registering with info={}, app info={}: {}',
                         self.server_params, self.app_params, e)
            self.accumulate_failure_count()
        return False

    def check_inited(self, authorization_key=None, app_id=None, app_secret=None):
        """检测是否注册到广目平台"""
        if not authorization_key:
            authorization_key = CONFIG.get('patronum', 'key')
        if not app_id:
            app_id = CONFIG.get('patronum', 'app_id')
        if not app_secret:
            app_secret = CONFIG.get('patronum', 'app_secret')
        if not self._server_info_inited:
            if not app_id or not app_secret or not authorization_key:
                logger.info('Unable to register patronum for lacking of '
                            'configuration, authorization_key={}, app_id={}',
                            authorization_key, app_id)
                return
            self.set_app_params(authorization_key, app_id, app_secret)
            if self.app_id and self.app_secret and self.authorization_key:
                self.__register_server()
        logger.info('Patronum wrapper inited, server id={}, token={}, '
                    'app id={}, app secret={}',
                    self.server_id, self.server_token,
                    self.app_id, self.app_secret)

    def update_host(self, host, authorization_key, app_id, app_token):
        """ Update Patronum host
        :param host: updated patronum host
        :param authorization_key: authorization key for updated patronum host
        :param app_id:
        :param app_token:
        :return status, message
        """
        if not host:
            return Error.PATRONUM_NOT_PROVIDED
        if not authorization_key:
            return Error.AUTHORIZATION_KEY_NOT_PROVIDED
        if not app_id or not app_token:
            return Error.APP_INFO_NOT_PROVIDED

        self.host = host
        original, self.host = self.host, host
        self.backup()
        try:
            self.set_app_params(authorization_key, app_id, app_token)
            self.__register_server()
        except ConnectionError:
            message = '{} is not a valid Patronum address'.format(host)
            logger.warning(message)
            self.host = original
            self.restore()
            return Error.create(0, message)
        except Exception as e:
            self.host = original
            self.restore()
            return Error.create(0, str(e))

        logger.info('Update Patronum address from {} to {}', original, host)
        return None


PATRONUM = PatronumWrapper()
PATRONUM.check_inited()

__all__ = [
    'PATRONUM'
]
