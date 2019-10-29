# -*- coding: utf-8 -*-
# @author: Chen Shijiang (dectincchen@sohu-inc.com)
# @date: 18-03-20 23:15
# @version: 1.0

"""图像缓存服务"""

from datetime import datetime
from os import path as osp
import threading

import cv2

from evision.lib.constant import Suffix
from evision.lib.log import logutil
from evision.lib.util import CacheUtil, PathUtil

from {{ cookiecutter.project_slug }}.util import paths

logger = logutil.get_logger()


def get_cache_path(directory=None, ext=Suffix.PNG):
    """生成随机缓存路径

    :param directory: 缓存文件夹
    :param ext: 文件扩展名
    :return: 缓存路径
    """
    if directory is None:
        directory = paths.media_path()

    now = datetime.now()
    tid = threading.get_ident()
    random_tail = CacheUtil.random_string(4)

    folder = now.strftime("%Y%m%d")
    filename = '{}_{}_{}.{}'.format(now.strftime("%y%m%d_%H%M%S%f"), tid,
                                    random_tail, ext)
    PathUtil.check_directory(osp.join(directory, folder))
    return osp.join(directory, folder, filename)


def fit(image, max_width, max_height):
    """根据图像尺寸限制缩放图像"""
    if image is None:
        return image
    scale = 1
    height, width, _ = image.shape
    if max_width:
        scale = min(float(max_width) / width, scale)
    if max_height:
        scale = max(float(max_height) / height, scale)
    if scale == 1:
        return image
    return cv2.resize(image, (int(width * scale), int(height * scale)))


def save_image(image_file, is_rgb=False, max_width=None, max_height=None, ext=Suffix.PNG):
    """保存图像

    :param image_file: 图像数据,numpy.ndarray格式
    :param is_rgb: 图像数据是否以RGB通道形式存储
    :param max_width: 保存图像的最大宽度
    :param max_height: 保存图像的最大高度
    :param ext: 保存图像拓展名
    :return: 图像存储路径
    """
    try:
        if image_file is None:
            return None
        if is_rgb:
            image_file = image_file[:, :, ::-1]
        if max_width or max_height:
            image_file = fit(image_file, max_width, max_height)
        _path = get_cache_path()
        cv2.imencode('.' + ext, image_file)[1].tofile(_path)
        return _path
    except Exception as e:
        logger.exception('Failed saving image file, shape={}: {}',
                         image_file.shape, e)
        return None
