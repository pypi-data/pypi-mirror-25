# -*- coding: utf-8 -*-

# Copyright(C) 2014 Romain Bignon
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.

import sys


__all__ = ['unicode', 'long', 'basestring', 'check_output', 'range',
           'with_metaclass',
           'quote', 'quote_plus', 'unquote', 'unquote_plus',
           'urlparse', 'urlunparse', 'urlsplit', 'urlunsplit',
           'urlencode', 'urljoin', 'parse_qs', 'parse_qsl',
          ]


try:
    unicode = unicode
except NameError:
    unicode = str

try:
    long = long
except NameError:
    long = int

try:
    basestring = basestring
except NameError:
    basestring = str


try:
    range = xrange
except NameError:
    range = range


from subprocess import check_output


try:
    from future.utils import with_metaclass
except ImportError:
    from six import with_metaclass


if sys.version_info.major == 2:
    class StrConv(object):
        def __str__(self):
            if hasattr(self, '__unicode__'):
                return self.__unicode__().encode('utf-8')
            else:
                return repr(self)
else:
    class StrConv(object):
        def __str__(self):
            if hasattr(self, '__unicode__'):
                return self.__unicode__()
            else:
                return repr(self)


try:
    from urllib import quote, quote_plus, unquote, unquote_plus, urlencode
    from urlparse import urlparse, urlunparse, urljoin, urlsplit, urlunsplit, parse_qsl, parse_qs
except ImportError:
    from urllib.parse import (
        urlparse, urlunparse, urlsplit, urlunsplit, urljoin, urlencode,
        quote, quote_plus, unquote, unquote_plus, parse_qsl, parse_qs,
    )
