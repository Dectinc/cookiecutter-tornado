#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 eVision.ai Inc. All Rights Reserved.
#
# @author: Chen Shijiang(chenshijiang@evision.ai)
# @date: 2019-10-29 21:41
# @version: 1.0
#
import requests
from tornado.httpclient import AsyncHTTPClient
import tornado.web

from evision.lib.tornado.handler import BaseHandler

class SamplePageHandler(tornado.web.RequestHandler):

    # @tornado.web.authenticated
    def get(self):
        self.render('index.html')


class SampleSynchronousFetchHandler(BaseHandler):
    def _get(self, *args, **kwargs):
        url = self.get_argument('url')
        response = requests.get(f'http://{url}')
        self.finish_response(result=response.text)


class SampleAsynchronousFetchHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        url = self.get_argument('url')
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(request=f'http://{url}')
        self.write(f'page content={response.body}')
