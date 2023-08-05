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


import re

from weboob.browser.pages import HTMLPage, LoggedPage
from weboob.browser.filters.standard import CleanText, CleanDecimal, Env, Format, TableCell, Date
from weboob.browser.elements import ListElement, ItemElement, TableElement, method
from weboob.browser.filters.html import Attr
from weboob.capabilities.bill import Bill, Document, Subscription
from weboob.capabilities.base import NotAvailable


class LoginPage(HTMLPage):
    def login(self, login, password):
        form = self.get_form('//form[@id="login"]')
        form['_username'] = login
        form['_password'] = password
        form.submit()


class ProfilPage(LoggedPage, HTMLPage):
    @method
    class get_list(ListElement):
        class item(ItemElement):
            klass = Subscription

            obj_subscriber = Format('%s %s', CleanText('//label[@for="form_firstname"]/../following-sibling::div'), CleanText('//label[@for="form_firstname"]/../following-sibling::div'))
            obj_id = Env('username')
            obj_label = obj_id

            def parse(self, el):
                self.env['username'] = self.page.browser.username


class DocumentsPage(LoggedPage, HTMLPage):
    @method
    class get_bills(TableElement):
        item_xpath = '//h3[contains(text(), "bills")]/following-sibling::table//tr[position() > 1]'
        head_xpath = '//h3[contains(text(), "bills")]/following-sibling::table//tr/th'

        col_id = u'Id'
        col_date = u'Date'
        col_price = u'Total TTC'

        class item(ItemElement):
            klass = Bill

            obj_id = Format('%s_%s', Env('username'), CleanDecimal(TableCell('id')))
            obj__url = Attr('.//a[contains(text(), "PDF")]', 'href', default=NotAvailable)
            obj_date = Date(CleanText(TableCell('date')))
            obj_format = u"pdf"
            obj_label = Format('Facture %s', CleanDecimal(TableCell('id')))
            obj_type = u"bill"
            obj_price = CleanDecimal(TableCell('price'))
            obj_currency = u"€"

            def condition(self):
                return CleanText(TableCell('id'))(self) != "No bills"

            def parse(self, el):
                self.env['username'] = self.page.browser.username


    @method
    class get_documents(ListElement):
        item_xpath = '//a[contains(@href, ".pdf")]'

        class item(ItemElement):
            klass = Document

            obj_id = Format('%s_%s', Env('username'), Env('docid'))
            obj__url = Attr('.', 'href')
            obj_format = u"pdf"
            obj_label = CleanText('.')
            obj_type = u"other"

            def parse(self, el):
                self.env['username'] = self.page.browser.username
                self.env['docid'] = re.sub('[^a-zA-Z0-9-_*.]', '', CleanText('.')(self))
