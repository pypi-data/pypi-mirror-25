# pylint: disable-msg=W0622
"""cubicweb-link packaging information"""

modname = 'link'
distname = "cubicweb-%s" % modname

numversion = (1, 8, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = "Logilab"
author_email = "contact@logilab.fr"
web = 'http://www.cubicweb.org/project/%s' % distname
description = "link component for the CubicWeb framework"
classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    ]

__depends__ = {'cubicweb': '>= 3.24.0'}
