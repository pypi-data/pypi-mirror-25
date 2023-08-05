# -*- coding: utf-8 -*-

# Copyright(C) 2016      Edouard Lambert
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


from weboob.tools.backend import AbstractModule, BackendConfig
from weboob.tools.value import ValueBackendPassword
from weboob.capabilities.bank import CapBank

from .browser import EsaliaBrowser


__all__ = ['EsaliaModule']


class EsaliaModule(AbstractModule, CapBank):
    NAME = 'esalia'
    DESCRIPTION = u'Société Générale Épargne Salariale'
    MAINTAINER = u'Edouard Lambert'
    EMAIL = 'elambert@budget-insight.com'
    LICENSE = 'AGPLv3+'
    VERSION = '1.3'
    CONFIG = BackendConfig(
             ValueBackendPassword('login',    label='Identifiant', masked=False),
             ValueBackendPassword('password', label='Code secret', regexp='^(\d{6})$'))

    BROWSER = EsaliaBrowser
    PARENT = 's2e'

    def create_default_browser(self):
        return self.create_browser(self.config['login'].get(),
                                   self.config['password'].get(),
                                   weboob=self.weboob)
