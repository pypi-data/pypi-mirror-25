# -*- coding: utf-8 -*-

# Copyright(C) 2012-2014 Vincent Paredes
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

from weboob.browser import LoginBrowser, URL, need_login
from weboob.exceptions import BrowserIncorrectPassword
from .pages import LoginPage, ProfilPage, BillsPage
from .pages.bills import SubscriptionsPage

__all__ = ['OrangeBillBrowser']


class OrangeBillBrowser(LoginBrowser):
    BASEURL = 'https://espaceclientv3.orange.fr/'

    loginpage = URL('https://id.orange.fr/auth_user/bin/auth_user.cgi', LoginPage)
    profilpage = URL('https://espaceclientv3.orange.fr/\?page=profil-infosPerso',
                     'https://espaceclientv3.orange.fr/ajax.php', ProfilPage)

    subscriptions = URL(r'https://espaceclientv3.orange.fr/js/necfe.php\?zonetype=bandeau&idPage=gt-home-page', SubscriptionsPage)

    subscriptions1 = URL(r'https://espaceclientv3.orange.fr/\?page=gt-home-page&orange&pro')
    subscriptions2 = URL(r'https://espaceclientv3.orange.fr/\?page=gt-home-page&sosh')

    billspage = URL('https://m.espaceclientv3.orange.fr/\?page=factures-archives',
                    'https://.*.espaceclientv3.orange.fr/\?page=factures-archives',
                    'https://espaceclientv3.orange.fr/\?page=factures-archives',
                    'https://espaceclientv3.orange.fr/\?page=facture-telecharger',
                    'https://espaceclientv3.orange.fr/maf.php',
                    'https://espaceclientv3.orange.fr/\?idContrat=(?P<subid>.*)&page=factures-historique',
                     BillsPage)

    def do_login(self):
        assert isinstance(self.username, basestring)
        assert isinstance(self.password, basestring)

        self.loginpage.stay_or_go().login(self.username, self.password)

        self.billspage.go()
        if self.loginpage.is_here():
            raise BrowserIncorrectPassword()

    def get_nb_remaining_free_sms(self):
        raise NotImplementedError()

    def post_message(self, message, sender):
        raise NotImplementedError()

    @need_login
    def get_subscription_list(self):
        ids = set()

        self.location('https://espaceclientv3.orange.fr/?page=gt-home-page&orange&pro')
        self.subscriptions.go()
        for sub in self.page.iter_subscription():
            ids.add(sub.id)
            yield sub

        self.location('https://espaceclientv3.orange.fr/?page=gt-home-page&sosh')
        self.subscriptions.go()
        for sub in self.page.iter_subscription():
            if sub.id not in ids:
                yield sub

    @need_login
    def iter_documents(self, subscription):
        documents = []
        for d in self.billspage.go(subid=subscription.id).get_documents(subid=subscription.id):
            documents.append(d)
        for b in self.billspage.go(subid=subscription.id).get_bills(subid=subscription.id):
            documents.append(b)
        return iter(documents)

