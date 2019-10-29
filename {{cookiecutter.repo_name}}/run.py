#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic run script"""

import asyncio
import signal
import time

import tornado.httpserver
import tornado.ioloop
from tornado.options import options
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
import tornado.web
import tornado.wsgi

from evision.lib.config import ConfigSection
from evision.lib.log import logutil

from {{ cookiecutter.project_slug }}.urls import url_patterns
from settings import APP_SETTINGS, CONFIG

logger = logutil.get_logger()

_start = time.time()


class TornadoInitialization(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **APP_SETTINGS)

    @staticmethod
    def start_services():
        logger.info('[Application] Starting main service...')

        logger.info('[Application] Service started')

    @staticmethod
    def stop_services():
        logger.info('[Application] Saving configuration...')
        CONFIG.save()

        logger.info('[Application] Stopping main service...')

        logger.info('[Application] Service stopped')


TORNADO_APP = TornadoInitialization()


def signal_handler(signum, frame):
    logger.info('Stopping server, with signum={}, frame={}', signum, frame)
    TORNADO_APP.stop_services()
    tornado.ioloop.IOLoop.instance().stop()

    import sys

    sys.exit()


def main():
    if CONFIG.getboolean(ConfigSection.TORNADO, 'auto_starting'):
        TORNADO_APP.start_services()
    if not options.port:
        options.port = CONFIG.getint('project', 'port')

    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
    http_server = tornado.httpserver.HTTPServer(TORNADO_APP)
    http_server.listen(options.port)
    print('Server inited, listening on {}, time elapsed: {:.4f}s'.format(
        options.port, time.time() - _start))
    signal.signal(signal.SIGINT, signal_handler)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

__all__ = [
    'TORNADO_APP',
    'main'
]
