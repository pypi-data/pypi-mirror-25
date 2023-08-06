# pylint: disable=W0622
"""cubicweb-postgis application packaging information"""

modname = 'postgis'
distname = 'cubicweb-postgis'

numversion = (0, 6, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Test for postgis'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb': '>= 3.24.0',
    'cwtags': '>= 1.1.0',
}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: JavaScript',
    'Topic :: Scientific/Engineering :: GIS',
    'Topic :: Database',
]
