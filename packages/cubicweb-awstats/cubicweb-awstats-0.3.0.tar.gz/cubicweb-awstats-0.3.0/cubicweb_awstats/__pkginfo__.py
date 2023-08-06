# pylint: disable=W0622
"""cubicweb-awstats application packaging information"""

modname = 'awstats'
distname = 'cubicweb-awstats'

numversion = (0, 3, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'cubicweb integrated awstats frontend'
web = 'https://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb': '>= 3.24.0',
    'six': None,
}
__recommends__ = {'cubicweb-raphael': None}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
