# -*- coding: utf-8 -*-

# Copyright(C) 2015      Vincent Paredes
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


from weboob.browser import LoginBrowser, URL, need_login
from weboob.exceptions import BrowserIncorrectPassword

from .pages import LoginPage, ProfilePage, BillsPage
from datetime import datetime, timedelta
import time

class OvhBrowser(LoginBrowser):
    BASEURL = 'https://www.ovh.com'

    login = URL('/auth/',
                '/manager/web/index.html', LoginPage)
    profile = URL('/engine/api/me', ProfilePage)
    documents = URL('/engine/2api/sws/billing/bills\?count=0&date=(?P<fromDate>.*)&dateTo=(?P<toDate>.*)&offset=0', BillsPage)

    def do_login(self):
        self.login.go()

        if self.page.is_logged():
            return

        self.page.login(self.username, self.password)

        self.page.check_double_auth()

        if not self.page.is_logged():
            raise BrowserIncorrectPassword

    @need_login
    def get_subscription_list(self):
        return self.profile.stay_or_go().get_list()

    @need_login
    def iter_documents(self, subscription):
        return self.documents.stay_or_go(fromDate=(datetime.now() - timedelta(days=2*365)).strftime("%Y-%m-%dT00:00:00Z"),
                                         toDate=time.strftime("%Y-%m-%dT%H:%M:%S.999Z")).get_documents(subid=subscription.id)
