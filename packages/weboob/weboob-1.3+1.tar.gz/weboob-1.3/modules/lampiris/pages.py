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


from weboob.browser.elements import ItemElement, ListElement, method
from weboob.browser.filters.html import Attr, CleanHTML, Link, XPathNotFound
from weboob.browser.filters.standard import CleanDecimal, CleanText, Date, Format
from weboob.browser.pages import HTMLPage
from weboob.capabilities.base import NotAvailable, Currency
from weboob.capabilities.bill import Bill, Subscription
from weboob.tools.compat import urljoin


class LoginPage(HTMLPage):
    def do_login(self, email, password):
        form = self.get_form(xpath='//form[@id="user-login"]')
        form['name'] = email
        form['pass'] = password
        form.submit()


class BillsPage(HTMLPage):
    @method
    class get_subscriptions(ListElement):
        item_xpath = '//div[@id="cusModal"]//div[has-class("cus-detail-wrapper")]'

        class item(ItemElement):
            klass = Subscription

            # TODO: Handle energy type
            obj_label = CleanText(CleanHTML('.'))
            obj_id = Attr('./input', 'value')

    @method
    class get_documents(ListElement):
        item_xpath = '//table[has-class("invoice-table-stickyheader")]/tbody/tr'

        class item(ItemElement):
            klass = Bill

            obj_id = Attr('./td[3]/span', 'title')
            obj_type = Format(
                '%s - %s',
                CleanText('./td[2]'),
                Attr('./td[1]//img', 'title')
            )
            obj_label = obj_type
            obj_format = 'pdf'
            obj_date = Date(CleanText('./td[4]'))
            obj_price = CleanDecimal('./td[5]', replace_dots=(' ', ','))
            def obj_currency(self):
                return Currency.get_currency(CleanText('./td[5]')(self))
            obj_duedate = Date(CleanText('./td[6]'))

            def obj_url(self):
                try:
                    return urljoin(
                        self.page.browser.BASEURL,
                        Link('./td[8]/a[1]')(self)
                    )
                except XPathNotFound:
                    return NotAvailable
