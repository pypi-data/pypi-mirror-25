# -*- coding: utf-8 -*-

# Copyright(C) 2015      James GALT
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

from random import randint
from weboob.browser import URL, LoginBrowser, need_login
from weboob.exceptions import BrowserIncorrectPassword

from .pages import LoginPage, IndexPage, BadLogin, AccountDetailPage, AccountHistoryPage


class AferBrowser(LoginBrowser):
    BASEURL = 'https://adherent.gie-afer.fr'
    VERIFY = 'afer.pem'

    login = URL('/web/ega.nsf/listeAdhesions\?OpenForm', LoginPage)
    bad_login = URL('/names.nsf\?Login', BadLogin)
    index = URL('/web/ega.nsf/listeAdhesions\?OpenForm', IndexPage)
    account_detail = URL('/web/ega.nsf/soldeEpargne\?openForm', AccountDetailPage)
    account_history = URL('/web/ega.nsf/generationSearchModule\?OpenAgent', AccountHistoryPage)
    history_detail = URL('/web/ega.nsf/WOpendetailOperation\?OpenAgent', AccountHistoryPage)

    def do_login(self):
        """
        Attempt to log in.
        Note: this method does nothing if we are already logged in.
        """
        assert isinstance(self.username, basestring)
        assert isinstance(self.password, basestring)
        self.login.go()

        self.page.login(self.username, self.password)
        if self.bad_login.is_here():
            raise BrowserIncorrectPassword()

    @need_login
    def iter_accounts(self):
        self.index.stay_or_go()
        return self.page.iter_accounts()

    @need_login
    def iter_investments(self, account):
        self.account_detail.go(params={'nads': account.id})
        return self.page.iter_investments()

    @need_login
    def iter_history(self, account):
        al = randint(0, 1000)
        data = {'cdeAdh': account.id, 'al': al, 'page': 1, 'form': 'F'}
        self.account_history.go(data={'cdeAdh': account.id, 'al': al, 'page': 1, 'form': 'F'})
        return self.page.iter_history(data=data)
