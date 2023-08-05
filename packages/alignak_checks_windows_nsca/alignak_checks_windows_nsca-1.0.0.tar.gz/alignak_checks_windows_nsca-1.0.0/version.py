#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
#   Frederic Mohier, frederic.mohier@alignak.net
#

"""
    Alignak - Checks pack for Windows NSCA monitored hosts/services
"""

# Package name
__pkg_name__ = u"alignak_checks_windows_nsca"

# Checks types for PyPI keywords
# Used for:
# - PyPI keywords
# - directory where to store files in the Alignak configuration (eg. arbiter/packs/checks_type)
__checks_type__ = u"windows-nsca"

# Application manifest
__version__ = u"1.0.0"
__author__ = u"Frédéric MOHIER"
__author_email__ = u"frederic.mohier@alignak.net"
__copyright__ = u"(c) 2015-2017 - %s" % __author__
__license__ = u"GNU Affero General Public License, version 3"
__git_url__ = u"https://github.com/Alignak-monitoring-contrib/alignak-checks-windows-nsca"
__doc_url__ = u"http://alignak-doc.readthedocs.io/en/latest"
__description__ = u"Alignak checks pack for Windows NSCA monitored hosts"

__classifiers__ = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Topic :: System :: Monitoring',
    'Topic :: System :: Systems Administration'
]
