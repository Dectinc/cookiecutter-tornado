# -*- coding: utf-8 -*-

from {{ cookiecutter.project_slug }}.handlers import sample


url_patterns = [
    (r"/sample/page", sample.SamplePageHandler),
    (r"/sample/fetch/sync", sample.SampleSynchronousFetchHandler),
    (r"/sample/fetch/async", sample.SampleAsynchronousFetchHandler)
]
