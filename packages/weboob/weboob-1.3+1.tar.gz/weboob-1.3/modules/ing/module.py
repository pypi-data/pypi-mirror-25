# -*- coding: utf-8 -*-

# Copyright(C) 2010-2014 Romain Bignon, Florent Fourcot
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
from datetime import timedelta

from weboob.capabilities.bank import CapBankTransfer, Account, AccountNotFound, RecipientNotFound
from weboob.capabilities.bill import CapDocument, Bill, Subscription,\
    SubscriptionNotFound, DocumentNotFound
from weboob.capabilities.profile import CapProfile
from weboob.capabilities.base import find_object, NotAvailable
from weboob.tools.backend import Module, BackendConfig
from weboob.tools.value import ValueBackendPassword, ValueDate
from weboob.browser.exceptions import ServerError

from .browser import IngBrowser

__all__ = ['INGModule']


class INGModule(Module, CapBankTransfer, CapDocument, CapProfile):
    NAME = 'ing'
    MAINTAINER = u'Florent Fourcot'
    EMAIL = 'weboob@flo.fourcot.fr'
    VERSION = '1.3'
    LICENSE = 'AGPLv3+'
    DESCRIPTION = 'ING Direct'
    CONFIG = BackendConfig(ValueBackendPassword('login',
                                                label=u'Numéro client',
                                                masked=False),
                           ValueBackendPassword('password',
                                                label='Code secret',
                                                regexp='^(\d{6})$'),
                           ValueDate('birthday',
                                     label='Date de naissance',
                                     formats=('%d%m%Y', '%d/%m/%Y', '%d-%m-%Y'))
                           )
    BROWSER = IngBrowser

    def create_default_browser(self):
        return self.create_browser(self.config['login'].get(),
                                   self.config['password'].get(),
                                   birthday=self.config['birthday'].get())

    def iter_resources(self, objs, split_path):
        if Account in objs:
            self._restrict_level(split_path)
            return self.iter_accounts()
        if Subscription in objs:
            self._restrict_level(split_path)
            return self.iter_subscription()

    def iter_accounts(self):
        return self.browser.get_accounts_list()

    def get_account(self, _id):
        return self.browser.get_account(_id)

    def iter_history(self, account):
        if not isinstance(account, Account):
            account = self.get_account(account)
        return self.browser.get_history(account)

    def iter_transfer_recipients(self, account):
        if not isinstance(account, Account):
            account = self.get_account(account)
        return self.browser.iter_recipients(account)

    def init_transfer(self, transfer, **params):
        self.logger.info('Going to do a new transfer')
        transfer.label = ' '.join(w for w in re.sub('[^0-9a-zA-Z/\-\?:\(\)\.,\'\+ ]+', '', transfer.label).split()).upper()
        if transfer.account_iban:
            account = find_object(self.iter_accounts(), iban=transfer.account_iban, error=AccountNotFound)
        else:
            account = find_object(self.iter_accounts(), id=transfer.account_id, error=AccountNotFound)

        if transfer.recipient_iban:
            recipient = find_object(self.iter_transfer_recipients(account.id), iban=transfer.recipient_iban, error=RecipientNotFound)
        else:
            recipient = find_object(self.iter_transfer_recipients(account.id), id=transfer.recipient_id, error=RecipientNotFound)

        return self.browser.init_transfer(account, recipient, transfer)

    def execute_transfer(self, transfer, **params):
        return self.browser.execute_transfer(transfer)

    def transfer_check_exec_date(self, old_exec_date, new_exec_date):
        return old_exec_date <= new_exec_date <= old_exec_date + timedelta(days=4)

    def iter_investment(self, account):
        if not isinstance(account, Account):
            account = self.get_account(account)
        return self.browser.get_investments(account)

    def iter_coming(self, account):
        if not isinstance(account, Account):
            account = self.get_account(account)
        return self.browser.get_coming(account)

    def iter_subscription(self):
        return self.browser.get_subscriptions()

    def get_subscription(self, _id):
        return find_object(self.browser.get_subscriptions(), id=_id, error=SubscriptionNotFound)

    def get_document(self, _id):
        subscription = self.get_subscription(_id.split('-')[0])
        return find_object(self.browser.get_documents(subscription), id=_id, error=DocumentNotFound)

    def iter_documents(self, subscription):
        if not isinstance(subscription, Subscription):
            subscription = self.get_subscription(subscription)
        return self.browser.get_documents(subscription)

    def download_document(self, bill):
        if not isinstance(bill, Bill):
            bill = self.get_document(bill)
        self.get_document(bill.id)
        try:
            self.browser.predownload(bill)
        except ServerError:
            return NotAvailable
        assert(self.browser.response.headers['content-type'] in ["application/pdf", "application/download"])
        return self.browser.response.content

    def get_profile(self):
        return self.browser.get_profile()
