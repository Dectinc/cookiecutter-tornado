#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 eVision.ai Inc. All Rights Reserved.
#
# @version: 1.0
#
import evision.lib.constant as evision_consts


class Keys(evision_consts.Keys):
    # Patronum
    EDIT_LIST = 'edit_list'
    DELETE_LIST = 'delete_list'
    IMAGE_LIST = 'image_list'
    PERSON_ID = 'person_id'
    PERSON_NAME = 'person_name'

    SERVER_ID = 'server_id'
    SERVER_TOKEN = 'server_token'
    APP_ID = 'app_id'
    APP_SECRET = 'app_secret'
    TIMESTAMP = 'timestamp'
    NOISE_STR = 'noise_str'
    SIGN = 'sign'


class _Error(object):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class Error(evision_consts.Error):
    # -60x Patronum api calling related errors
    PATRONUM_NOT_PROVIDED = _Error(-601, '未提供广目平台地址')
    """
    @apiDefine PatronumNotProvidedError
    @apiError (ValueError) {json} PatronumNotProvidedError 未提供广目平台地址
    @apiErrorExample {json} PatronumNotProvidedError-Response:
        HTTP/1.1 200
        {
            "status": -601,
            "message": "未提供广目平台地址"
        }
    """

    AUTHORIZATION_KEY_NOT_PROVIDED = _Error(-602, '未提供广目平台授权秘钥')
    """
    @apiDefine AuthorizationKeyNotProvidedError
    @apiError (ValueError) {json} AuthorizationKeyNotProvidedError 未提供广目平台授权秘钥
    @apiErrorExample {json} AuthorizationKeyNotProvidedError-Response:
        HTTP/1.1 200
        {
            "status": -602,
            "message": "未提供广目平台授权秘钥"
        }
    """

    PATRONUM_NOT_UPDATED = _Error(-603, '广目平台地址未更新')
    """
    @apiDefine PatronumNotUpdatedError
    @apiError (ValueError) {json} PatronumNotUpdatedError 广目平台地址未更新
    @apiErrorExample {json} PatronumNotUpdatedError-Response:
        HTTP/1.1 200
        {
            "status": -603,
            "message": "广目平台地址未更新"
        }
    """

    PATRONUM_FAILED_UPLOADING = _Error(-604, '上传图像到广目平台失败')
    """
    @apiDefine PatronumFailedUploadingError
    @apiError (Failed) {json} PatronumFailedUploadingError 上传图像到广目平台失败
    @apiErrorExample {json} PatronumFailedUploadingError-Response:
        HTTP/1.1 200
        {
            "status": -604,
            "message": "上传图像到广目平台失败"
        }
    """

    PATRONUM_FAILED_ACCESSING = _Error(-605, '调用广目平台API失败')
    """
    @apiDefine PatronumFailedAccessingError
    @apiError (Failed) {json} PatronumFailedAccessingError 调用广目平台API失败
    @apiErrorExample {json} PatronumFailedAccessingError-Response:
        HTTP/1.1 200
        {
            "status": -605,
            "message": "调用广目平台API失败"
        }
    """

    APP_INFO_NOT_PROVIDED = _Error(-606, '未提供APP ID或APP SECRET')
    """
    @apiDefine AppInfoNotProvidedError
    @apiError (ValueError) {json} AppInfoNotProvidedError 未提供APP ID或APP SECRET
    @apiErrorExample {json} AppInfoNotProvidedError-Response:
        HTTP/1.1 200
        {
            "status": -606,
            "message": "未提供APP ID或APP SECRET"
        }
    """
