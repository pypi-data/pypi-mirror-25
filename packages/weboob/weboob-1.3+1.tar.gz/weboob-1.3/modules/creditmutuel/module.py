# -*- coding: utf-8 -*-

# Copyright(C) 2010-2011 Julien Veyssier
# Copyright(C) 2012-2013 Romain Bignon
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


from decimal import Decimal

from weboob.capabilities.base import find_object
from weboob.capabilities.bank import CapBankTransferAddRecipient, AccountNotFound, RecipientNotFound, \
                                     Account, TransferError
from weboob.capabilities.contact import CapContact
from weboob.capabilities.profile import CapProfile
from weboob.tools.backend import Module, BackendConfig
from weboob.tools.value import ValueBackendPassword

from .browser import CreditMutuelBrowser


__all__ = ['CreditMutuelModule']


class CreditMutuelModule(Module, CapBankTransferAddRecipient, CapContact, CapProfile):
    NAME = 'creditmutuel'
    MAINTAINER = u'Julien Veyssier'
    EMAIL = 'julien.veyssier@aiur.fr'
    VERSION = '1.3'
    DESCRIPTION = u'Crédit Mutuel'
    LICENSE = 'AGPLv3+'
    CONFIG = BackendConfig(ValueBackendPassword('login',    label='Identifiant', masked=False),
                           ValueBackendPassword('password', label='Mot de passe'))
    BROWSER = CreditMutuelBrowser

    def create_default_browser(self):
        return self.create_browser(self.config['login'].get(), self.config['password'].get())

    def iter_accounts(self):
        for account in self.browser.get_accounts_list():
            yield account

    def get_account(self, _id):
        account = self.browser.get_account(_id)
        if account:
            return account
        else:
            raise AccountNotFound()

    def iter_coming(self, account):
        for tr in self.browser.get_history(account):
            if tr._is_coming:
                yield tr

    def iter_history(self, account):
        for tr in self.browser.get_history(account):
            if not tr._is_coming:
                yield tr

    def iter_investment(self, account):
        return self.browser.get_investment(account)

    def iter_transfer_recipients(self, origin_account):
        if not self.browser.is_new_website:
            raise NotImplementedError()

        if not isinstance(origin_account, Account):
            origin_account = find_object(self.iter_accounts(), id=origin_account, error=AccountNotFound)
        return self.browser.iter_recipients(origin_account)

    def new_recipient(self, recipient, **params):
        return self.browser.new_recipient(recipient, **params)

    def init_transfer(self, transfer, **params):
        # There is a check on the website, transfer can't be done with too long reason.
        if transfer.label:
            transfer.label = transfer.label[:27]

        self.logger.info('Going to do a new transfer')
        if transfer.account_iban:
            account = find_object(self.iter_accounts(), iban=transfer.account_iban, error=AccountNotFound)
        else:
            account = find_object(self.iter_accounts(), id=transfer.account_id, error=AccountNotFound)

        if transfer.recipient_iban:
            recipient = find_object(self.iter_transfer_recipients(account.id), iban=transfer.recipient_iban, error=RecipientNotFound)
        else:
            recipient = find_object(self.iter_transfer_recipients(account.id), id=transfer.recipient_id, error=RecipientNotFound)

        try:
            assert account.id.isdigit()
            # quantize to show 2 decimals.
            amount = Decimal(transfer.amount).quantize(Decimal(10) ** -2)
        except (AssertionError, ValueError):
            raise TransferError('something went wrong')

        return self.browser.init_transfer(account, recipient, amount, transfer.label)

    def execute_transfer(self, transfer, **params):
        return self.browser.execute_transfer(transfer)

    def iter_contacts(self):
        return self.browser.get_advisor()

    def get_profile(self):
        if not hasattr(self.browser, 'get_profile'):
            raise NotImplementedError()
        return self.browser.get_profile()
