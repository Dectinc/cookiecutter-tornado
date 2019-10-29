# -*- coding: utf-8 -*-

import tornado.web

from evision.lib.log import logutil

from {{ cookiecutter.project_slug }}.handlers import sample
from {{ cookiecutter.project_slug }}.util import paths

from .version import __version__

logger = logutil.get_logger()

_API_VERSION = __version__.split('.')[2]
def __url(*a, version=_API_VERSION):
    return r'/' + r'/'.join([r'{{ cookiecutter.project_slug }}', r'v{}'.format(version)]
                            + [str(_) for _ in a])

url_patterns = [
    (r"/sample/page", sample.SamplePageHandler),
    (r"/sample/fetch/sync", sample.SampleSynchronousFetchHandler),
    (r"/sample/fetch/async", sample.SampleAsynchronousFetchHandler),
    (__url('docs', '(.*)'), tornado.web.StaticFileHandler, {'path': paths.DOC_ROOT, 'default_filename': 'index.html'})
]

logger.info('=' * 40)
logger.info('= Setting url patterns')
logger.info('=' * 40)
for url_pattern in sorted(url_patterns):
    logger.info('Mapping {} => {}', url_pattern[0], url_pattern[1])
logger.info('=' * 40)
logger.info('= Set url patterns done')
logger.info('=' * 40)
