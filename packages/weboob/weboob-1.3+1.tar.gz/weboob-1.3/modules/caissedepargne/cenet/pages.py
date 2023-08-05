# -*- coding: utf-8 -*-

# Copyright(C) 2012 Romain Bignon
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
import json

from weboob.browser.pages import LoggedPage, HTMLPage, JsonPage
from weboob.browser.elements import DictElement, ItemElement, method
from weboob.browser.filters.standard import Date, CleanDecimal, CleanText, Format, Field
from weboob.browser.filters.json import Dict
from weboob.capabilities import NotAvailable
from weboob.capabilities.bank import Account, Transaction
from weboob.capabilities.contact import Advisor
from weboob.capabilities.profile import Profile
from weboob.tools.capabilities.bank.transactions import FrenchTransaction
from weboob.exceptions import BrowserUnavailable


class LoginPage(JsonPage):
    def get_response(self):
        return self.doc


class CenetLoginPage(HTMLPage):
    def login(self, username, password, nuser, codeCaisse, _id, vkpass):
        form = self.get_form(id='aspnetForm')

        form['__EVENTTARGET'] = "btn_authentifier_securise"
        form['__EVENTARGUMENT'] = '{"CodeCaisse":"%s","NumeroBad":"%s","NumeroUsager":"%s",\
                                    "MotDePasse":"%s","IdentifiantClavier":"%s","ChaineConnexion":"%s"}' \
                                    % (codeCaisse, username, nuser, password, _id, vkpass)

        form.submit()


class CenetHomePage(HTMLPage):
    @method
    class get_advisor(ItemElement):
        klass = Advisor

        obj_name = CleanText('//section[contains(@id, "ChargeAffaires")]//strong')
        obj_email = CleanText('//li[contains(@id, "MailContact")]')
        obj_phone = CleanText('//li[contains(@id, "TelAgence")]', replace=[('.', '')])
        obj_mobile = NotAvailable
        obj_agency = CleanText('//section[contains(@id, "Agence")]//strong')
        obj_address = CleanText('//li[contains(@id, "AdresseAgence")]')

        def obj_fax(self):
            return CleanText('//li[contains(@id, "FaxAgence")]', replace=[('.', '')])(self) or NotAvailable

    @method
    class get_profile(ItemElement):
        klass = Profile

        obj_name = CleanText('//li[@class="identite"]/a/span')


class CenetJsonPage(JsonPage):
    def __init__(self, browser, response, *args, **kwargs):
        super(CenetJsonPage, self).__init__(browser, response, *args, **kwargs)

        # Why you are so ugly....
        self.doc = json.loads(self.doc['d'])
        if self.doc['Erreur'] and self.doc['Erreur']['Titre']:
            self.logger.warning('error on %r: %s', self.url, self.doc['Erreur']['Titre'])
            raise BrowserUnavailable(self.doc['Erreur']['Titre'])

        self.doc['DonneesSortie'] = json.loads(self.doc['DonneesSortie'])


class CenetAccountsPage(LoggedPage, CenetJsonPage):
    ACCOUNT_TYPES = {u'CCP': Account.TYPE_CHECKING}

    @method
    class get_accounts(DictElement):
        item_xpath = "DonneesSortie"

        class item(ItemElement):
            klass = Account

            obj_id = CleanText(Dict('Numero'))
            obj_label = CleanText(Dict('Intitule'))
            obj_iban = CleanText(Dict('IBAN'))

            def obj_balance(self):
                absolut_amount = CleanDecimal(Dict('Solde/Valeur'))(self)
                if CleanText(Dict('Solde/CodeSens'))(self) == 'D':
                    return -absolut_amount
                return absolut_amount


            def obj_currency(self):
                return CleanText(Dict('Devise'))(self).upper()

            def obj_type(self):
                return self.page.ACCOUNT_TYPES.get(Dict('TypeCompte')(self), Account.TYPE_UNKNOWN)

            def obj__formated(self):
                return self.el


class CenetCardsPage(LoggedPage, CenetJsonPage):
    def get_cards(self):
        cards = Dict('DonneesSortie')(self.doc)

        # Remove dates to prevent bad parsing
        def reword_dates(card):
            tmp_card = card

            for k, v in tmp_card.items():
                if isinstance(v, dict):
                    v = reword_dates(v)
                if k == "Date" and v is not None and "Date" in v:
                    card[k] = None

        for card in cards:
            reword_dates(card)

        return cards

class CenetAccountHistoryPage(LoggedPage, CenetJsonPage):
    TR_TYPES = {8: Transaction.TYPE_TRANSFER, # VIR
                7: Transaction.TYPE_TRANSFER, # VIR COMPTE A COMPTE
                6: Transaction.TYPE_CASH_DEPOSIT, # REMISE CHECQUE(s)
                4: Transaction.TYPE_ORDER # PRELV
                }

    @method
    class get_history(DictElement):
        item_xpath = "DonneesSortie"

        class item(ItemElement):
            klass = Transaction

            obj_raw = Format('%s %s', Dict('Libelle'), Dict('Libelle2'))
            obj_label = CleanText(Dict('Libelle'))
            obj_date = Date(Dict('DateGroupImputation'), dayfirst=True)
            obj_rdate = Date(Dict('DateGroupReglement'), dayfirst=True)

            def obj_type(self):
                ret = self.page.TR_TYPES.get(Dict('TypeMouvement')(self), Transaction.TYPE_UNKNOWN)
                if ret != Transaction.TYPE_UNKNOWN:
                    return ret

                for pattern, type in Transaction.PATTERNS:
                    if pattern.match(Field('raw')(self)):
                        return type

                return Transaction.TYPE_UNKNOWN

            def obj_original_currency(self):
                return CleanText(Dict('Montant/Devise'))(self).upper()

            def obj_amount(self):
                amount = CleanDecimal(Dict('Montant/Valeur'))(self)

                return -amount if Dict('Montant/CodeSens')(self) == "D" else amount

    def next_offset(self):
        offset = Dict('OffsetSortie')(self.doc)
        if offset:
            assert Dict('EstComplete')(self.doc) == 'false'
        return offset


class _LogoutPage(HTMLPage):
    def on_load(self):
        raise BrowserUnavailable(CleanText('//*[@class="messErreur"]')(self.doc))


class ErrorPage(_LogoutPage):
    pass


class UnavailablePage(HTMLPage):
    def on_load(self):
        raise BrowserUnavailable(CleanText('//div[@id="message_error_hs"]')(self.doc))


class Transaction(FrenchTransaction):
    PATTERNS = [(re.compile('^CB (?P<text>.*?) FACT (?P<dd>\d{2})(?P<mm>\d{2})(?P<yy>\d{2})', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_CARD),
                (re.compile('^RET(RAIT)? DAB (?P<dd>\d+)-(?P<mm>\d+)-.*', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_WITHDRAWAL),
                (re.compile('^RET(RAIT)? DAB (?P<text>.*?) (?P<dd>\d{2})(?P<mm>\d{2})(?P<yy>\d{2}) (?P<HH>\d{2})H(?P<MM>\d{2})', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_WITHDRAWAL),
                (re.compile('^VIR(EMENT)?(\.PERIODIQUE)? (?P<text>.*)', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_TRANSFER),
                (re.compile('^PRLV (?P<text>.*)', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_ORDER),
                (re.compile('^CHEQUE.*', re.IGNORECASE),    FrenchTransaction.TYPE_CHECK),
                (re.compile('^(CONVENTION \d+ )?COTIS(ATION)? (?P<text>.*)', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_BANK),
                (re.compile(r'^\* (?P<text>.*)', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_BANK),
                (re.compile('^REMISE (?P<text>.*)', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_DEPOSIT),
                (re.compile('^(?P<text>.*)( \d+)? QUITTANCE .*', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_ORDER),
                (re.compile('^CB [\d\*]+ TOT DIF .*', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_CARD_SUMMARY),
                (re.compile('^CB [\d\*]+ (?P<text>.*)', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_CARD),
                (re.compile('^CB (?P<text>.*?) (?P<dd>\d{2})(?P<mm>\d{2})(?P<yy>\d{2})', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_CARD),
                (re.compile('\*CB (?P<text>.*?) (?P<dd>\d{2})(?P<mm>\d{2})(?P<yy>\d{2})', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_CARD),
                (re.compile('^FAC CB (?P<text>.*?) (?P<dd>\d{2})/(?P<mm>\d{2})', re.IGNORECASE),
                                                            FrenchTransaction.TYPE_CARD),
               ]
