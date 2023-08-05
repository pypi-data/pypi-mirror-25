# -*- coding: utf-8 -*-

# Copyright(C) 2017      Phyks (Lucas Verney)
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

from __future__ import unicode_literals


from weboob.tools.backend import Module
from weboob.capabilities.housing import CapHousing

from .browser import FonciaBrowser


__all__ = ['FonciaModule']


class FonciaModule(Module, CapHousing):
    NAME = 'foncia'
    DESCRIPTION = u'Foncia housing website.'
    MAINTAINER = u'Phyks (Lucas Verney)'
    EMAIL = 'phyks@phyks.me'
    LICENSE = 'AGPLv3+'
    VERSION = '1.3'

    BROWSER = FonciaBrowser

    def get_housing(self, housing):
        return self.browser.get_housing(housing)

    def search_city(self, pattern):
        return self.browser.get_cities(pattern)

    def search_housings(self, query):
        cities = ','.join(
            ['%s' % c.name for c in query.cities if c.backend == self.name]
        )
        if len(cities) == 0:
            return []

        return self.browser.search_housings(query, cities)
