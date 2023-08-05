# -*- coding: utf-8 -*-

# Copyright(C) 2017 Vincent Ardisson
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

from ast import literal_eval
from decimal import Decimal
import re

from weboob.browser.pages import LoggedPage, JsonPage, HTMLPage
from weboob.browser.elements import ItemElement, DictElement, method
from weboob.browser.filters.standard import Date, Eval, CleanDecimal, CleanText
from weboob.browser.filters.json import Dict
from weboob.capabilities.bank import Account, Transaction
from weboob.capabilities.base import NotAvailable
from weboob.tools.json import json


def flatten(l):
    if not isinstance(l, list):
        yield l
        return

    for e in l:
        for s in flatten(e):
            yield s


def float_to_decimal(f):
    return Decimal(str(f))


class DashboardPage(LoggedPage, HTMLPage):
    pass


class AccountsPage3(LoggedPage, HTMLPage):
    def iter_accounts(self):
        for line in self.doc.xpath('//script[@id="initial-state"]')[0].text.split('\n'):
            m = re.search('window.__INITIAL_STATE__ = (.*);', line)
            if m:
                data = list(flatten(json.loads(literal_eval(m.group(1)))))
                break
        else:
            assert False, "data was not found"

        assert data.count('display_account_number') == 1, 'there should be exactly one card'

        acc = Account()
        acc.id = 'XXX-%s' % data[1 + data.index('display_account_number')]
        acc.label = '%s %s' % (data[1 + data.index('description')], data[1 + data.index('embossed_name')])
        acc._index = data[1 + data.index('sorted_index')]
        acc._token = data[1 + data.index('account_token')]
        yield acc


class JsonBalances(LoggedPage, JsonPage):
    def set_balances(self, accounts):
        by_token = {a._token: a for a in accounts}
        for d in self.doc:
            by_token[d['account_token']].coming = -float_to_decimal(d['total_debits_balance_amount'])
            by_token[d['account_token']].balance = -float_to_decimal(d['total_payments_credits_amount'])


class JsonPeriods(LoggedPage, JsonPage):
    def get_periods(self):
        return [(p['statement_start_date'], p['statement_end_date']) for p in self.doc]


class JsonHistory(LoggedPage, JsonPage):
    def get_count(self):
        return self.doc['total_count']

    @method
    class iter_history(DictElement):
        item_xpath = 'transactions'

        class item(ItemElement):
            klass = Transaction

            obj_type = Transaction.TYPE_DEFERRED_CARD
            obj_raw = CleanText(Dict('description'))
            obj_date = Date(Dict('statement_end_date', default=None), default=None)
            obj_rdate = Date(Dict('charge_date'))
            obj_vdate = Date(Dict('post_date', default=None), default=NotAvailable)
            obj_amount = Eval(lambda x: -float_to_decimal(x), Dict('amount'))
            obj_original_currency = Dict('foreign_details/iso_alpha_currency_code', default=NotAvailable)
            obj_original_amount = CleanDecimal(Dict('foreign_details/amount', default=NotAvailable), sign=lambda x: -1, default=NotAvailable)

            #obj__ref = Dict('reference_id')
            obj__ref = Dict('identifier')
