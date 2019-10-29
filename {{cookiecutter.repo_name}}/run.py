#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Basic run script"""

import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import options

from settings import APP_SETTINGS

from {{cookiecutter.project_slug}}.urls import url_patterns

class TornadoApplication(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **APP_SETTINGS)


def main():
    app = TornadoApplication()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
