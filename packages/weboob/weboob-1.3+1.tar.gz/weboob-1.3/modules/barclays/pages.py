# -*- coding: utf-8 -*-

# Copyright(C) 2012-2017 Jean Walrave
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

import re

from weboob.browser.pages import HTMLPage, PDFPage, LoggedPage
from weboob.browser.elements import TableElement, ListElement, ItemElement, method
from weboob.browser.filters.standard import CleanText, CleanDecimal, Regexp, Field, TableCell, Date, Eval
from weboob.browser.filters.html import Attr
from weboob.capabilities.bank import Account, Investment, NotAvailable
from weboob.tools.capabilities.bank.transactions import FrenchTransaction
from weboob.tools.capabilities.bank.iban import is_iban_valid


def MyDecimal(*args, **kwargs):
    kwargs.update(replace_dots=True, default=NotAvailable)
    return CleanDecimal(*args, **kwargs)


class StatefulPage(LoggedPage, HTMLPage):
    def get_form_for_menu(self, menu):
        btn = Regexp(Attr('//div[@class="menuvert"]//a[contains(., "%s")]' % (menu), 'onclick'), r"\('', '(.*?)',")(self.doc)
        form = self.get_form(id='form1')
        form['MODE'] = 'NAVMENU_' + btn
        return form

    def go_to_menu(self, menu):
        form = self.get_form_for_menu(menu)
        form.submit()

    def go_to_account(self, account):
        token = self.isolate_token()

        form = self.get_form(id='form1')

        for attr in list(form):
            if attr not in ['MENUSTATE', 'DEVICE_SIZE_INFO', 'C11__GETMODULENOTEPAD[1].IOGETMODULENOTEPAD[1].OUTPUTPARAMETER[1].TEXT', token[0]]:
                del form[attr]

        form['MODE'] = account._btn
        form['C4__AUTOSELECTOR_TBL_4F9C27E5D4E67F554398'] = account._btn[-1]
        form['C4__AUTOSELECTOR_TBL_DASHBOARD'] = account._btn[-3]

        form.submit()

    def isolate_token(self):
        return (Attr('(//input[@type="hidden"])[2]', 'name')(self.doc), Attr('(//input[@type="hidden"])[2]', 'value')(self.doc))


class LoginPage(HTMLPage):
    def is_here(self):
        return bool(CleanText('//div[@class="zone-authent"]')(self.doc))

    def login(self, login, passwd):
        form = self.get_form(id='form1')

        form['MODE'] = 'C1____09AE2D522D145CD3 FormButton 27'
        form['C1__IOPARAMETERWS[1].INPUTPARAMETER[1].LOGINID'] = login
        form['C1__IOPARAMETERWS[1].INPUTPARAMETER[1].PASSWORD'] = passwd

        form.submit()

    def login_secret(self, secret):
        label = CleanText('//label[@for="C1__IdTwoLetters"]')(self.doc).strip()

        letters = ''
        for n in re.findall('(\d+)', label):
            letters += secret[int(n) - 1]

        form = self.get_form(id='form1')

        form['MODE'] = 'C1____09AE2D522D145CD3 FormButton 29'
        form['C1__IOPARAMETERWS[1].INPUTPARAMETER[1].LETTERSSECSUP'] = letters

        form.submit()

    def has_error(self):
        return bool(CleanText('//div[@class="bloc-message error" and not(@style)]')(self.doc))


class AccountsPage(StatefulPage):
    ACCOUNT_TYPES = {'Liquidités': Account.TYPE_CHECKING,
                     'Epargne': Account.TYPE_SAVINGS,
                     'Titres': Account.TYPE_MARKET,
                     'Engagement/Crédits': Account.TYPE_LOAN,
                    }
    ACCOUNT_EXTRA_TYPES = {'BMOOVIE': Account.TYPE_LIFE_INSURANCE
                          }
    ACCOUNT_TYPE_TO_STR = {Account.TYPE_MARKET: 'TTR',
                           Account.TYPE_CARD: 'CRT'
                          }

    def is_here(self):
        return bool(self.doc.xpath('//h1[contains(., "Mes comptes")]'))

    @method
    class iter_accounts(ListElement):
        item_xpath = u'//tr[contains(@id, "C4__p0_TBL_DASHBOARD")]'

        class item(ItemElement):
            klass = Account

            obj_balance = MyDecimal('.//td[4]//div[1]/a')
            obj_label = CleanText('.//td[1]//span')
            obj__uncleaned_id = CleanText('.//td[2]//a')
            obj__btn = Attr('.//button', 'name', default=None)
            obj__attached_account = NotAvailable # for card account only

            def obj_id(self):
                return re.sub(r'\s', '', str(Field('_uncleaned_id')(self))) + self.page.ACCOUNT_TYPE_TO_STR.get(Field('type')(self), '')

            def obj_currency(self):
                return Account.get_currency(CleanText('.//td[5]//div[1]/a')(self))

            def obj_type(self):
                if self.xpath('.//div[contains(@id, "9385968FC88E7527131931") and not(contains(@style, "display: none;"))]'):
                    return Account.TYPE_CARD

                type = CleanText('./ancestor::node()[7]//button[contains(@id, "C4__BUT_787E7BC48BF75E723710")]')(self)

                return self.page.ACCOUNT_EXTRA_TYPES.get(Field('label')(self)) or self.page.ACCOUNT_TYPES.get(type, Account.TYPE_UNKNOWN)

            def obj__multiple_type(self):
                # Sometime account can be twice declared with different types but same id, we flag them to avoid some errors
                for account in self.parent.objects.values():
                    if account._uncleaned_id == Field('_uncleaned_id')(self):
                        if not account._multiple_type:
                            account._multiple_type = True

                        return True

                return False

            def validate(self, el):
                return Field('type')(self) != Account.TYPE_UNKNOWN


class Transaction(FrenchTransaction):
    PATTERNS = [(re.compile('^RET DAB (?P<text>.*?) RETRAIT DU (?P<dd>\d{2})(?P<mm>\d{2})(?P<yy>\d{2}).*'),
                                                              FrenchTransaction.TYPE_WITHDRAWAL),
                (re.compile('^RET DAB (?P<text>.*?) CARTE ?:.*'),
                                                              FrenchTransaction.TYPE_WITHDRAWAL),
                (re.compile('^RET DAB (?P<dd>\d{2})/(?P<mm>\d{2})/(?P<yy>\d{2}) (?P<text>.*?) CARTE .*'),
                                                              FrenchTransaction.TYPE_WITHDRAWAL),
                (re.compile('^(?P<text>.*) RETRAIT DU (?P<dd>\d{2})(?P<mm>\d{2})(?P<yy>\d{2}) .*'),
                                                              FrenchTransaction.TYPE_WITHDRAWAL),
                (re.compile('(\w+) (?P<dd>\d{2})(?P<mm>\d{2})(?P<yy>\d{2}) CB[:\*][^ ]+ (?P<text>.*)'),
                                                              FrenchTransaction.TYPE_CARD),
                (re.compile('^(?P<category>VIR(EMEN)?T? (SEPA)?(RECU|FAVEUR)?)( /FRM)?(?P<text>.*)'),
                                                              FrenchTransaction.TYPE_TRANSFER),
                (re.compile('^PRLV (?P<text>.*) (REF: .*)?$'),FrenchTransaction.TYPE_ORDER),
                (re.compile('^CHEQUE.*? (REF \w+)?$'),        FrenchTransaction.TYPE_CHECK),
                (re.compile('^(AGIOS /|FRAIS) (?P<text>.*)'), FrenchTransaction.TYPE_BANK),
                (re.compile('^(CONVENTION \d+ )?COTIS(ATION)? (?P<text>.*)'),
                                                              FrenchTransaction.TYPE_BANK),
                (re.compile('^REMISE (?P<text>.*)'),          FrenchTransaction.TYPE_DEPOSIT),
                (re.compile('^(?P<text>.*)( \d+)? QUITTANCE .*'),
                                                              FrenchTransaction.TYPE_ORDER),
                (re.compile('^.* LE (?P<dd>\d{2})/(?P<mm>\d{2})/(?P<yy>\d{2})$'),
                                                              FrenchTransaction.TYPE_UNKNOWN),
                (re.compile('^CARTE .*'), FrenchTransaction.TYPE_CARD_SUMMARY)
               ]


class AbstractAccountPage(StatefulPage):
    def has_iban(self):
        return len(self.doc.xpath('//a[contains(., "Edition RIB")]/ancestor::node()[2][not(contains(@style, "display: none;"))]')) > 1

    def has_history(self):
        return bool(self.doc.xpath(u'//div[contains(@id, "83B48AC016951684534547") and contains(@style, "display: none;")]'))

    def form_to_history_page(self):
        btn = Attr('//button[contains(@id, "moreOperations")]', 'name', default=NotAvailable)(self.doc)

        if btn is NotAvailable:
            return

        token = self.isolate_token()
        form = self.get_form(id='form1')

        for attr in list(form):
            if attr not in ['MENUSTATE', 'DEVICE_SIZE_INFO', 'C4__WORKING[1].IDENTINTCONTRAT', 'C9__GETMODULENOTEPAD[1].IOGETMODULENOTEPAD[1].OUTPUTPARAMETER[1].TEXT', token[0]]:
                del form[attr]

        form['MODE'] = btn

        return form

    @method
    class iter_history(TableElement):
        head_xpath = '//table[@class="table_operations"]/thead/tr/th//a/text()'
        item_xpath = '//table[@class="table_operations"]/tbody/tr'

        col_date = u'Date Opération'
        col_vdate = 'Date valeur'
        col_debit = u'Débit'
        col_credit = u'Crédit'

        class item(ItemElement):
            klass = Transaction

            obj_date = Date(CleanText(TableCell('date')), dayfirst=True)
            obj_raw = Transaction.Raw('./td[2]//span[contains(@id, "4F6C8C3CD61D40A615776")]')
            obj_vdate = Date(CleanText(TableCell('vdate')), dayfirst=True)
            obj_amount = MyDecimal(TableCell('credit'), default=TableCell('debit'))


class AccountPage(AbstractAccountPage):
    def is_here(self):
        return bool(CleanText('//select[@name="C4__WORKING[1].IDENTINTCONTRAT"]')(self.doc))


class MarketAccountPage(AbstractAccountPage):
    def is_here(self):
        return bool(self.doc.xpath('//select[@name="C4__WORKING[1].SELECTEDSECURITYACCOUNTID"]'))

    def get_space_attrs(self, space):
        a = Regexp(Attr('//a[contains(span, "%s")]' % space, 'onclick'), r'\((.*?)\)')(self.doc).replace('\'', '').split(', ')
        form = self.get_form(id='form1')

        return (a[1], 'C4__WORKING[1].SELECTEDSECURITYACCOUNTID', form['C4__WORKING[1].SELECTEDSECURITYACCOUNTID'], a[2])

    def iter_investments(self):
        raise NotImplementedError()


class LifeInsuranceAccountPage(AbstractAccountPage):
    def is_here(self):
        return bool(CleanText('//select[@name="C4__WORKING[1].IDENTCONTRACTLIST"]')(self.doc))

    def has_history(self):
        return True

    def get_space_attrs(self, space):
        a = Regexp(Attr('//a[contains(span, "%s")]' % space, 'onclick'), r'\((.*?)\)')(self.doc).replace('\'', '').split(', ')
        form = self.get_form(id='form1')

        return (a[1], 'C4__WORKING[1].IDENTCONTRACTLIST', form['C4__WORKING[1].IDENTCONTRACTLIST'], a[2])

    @method
    class iter_history(TableElement):
        head_xpath = '//table[@id="C4__TBL_MVT"]/thead/tr/th//a/text()'
        item_xpath = '//table[@id="C4__TBL_MVT"]/tbody/tr'

        col_label = u'Opération'
        col_vdate = u'Date d\'effet'
        col_amount = u'Montant net'

        class item(ItemElement):
            klass = Transaction

            obj_raw = Transaction.Raw(TableCell('label'))
            obj_vdate = Date(CleanText(TableCell('vdate')), dayfirst=True)

            def obj_amount(self):
                return MyDecimal('.//div/span')(TableCell('amount')(self)[0])

            def obj_date(self):
                return Date(CleanText('.//span[contains(@id, "C4__QUE_50FADFF19F566198286748")]'), dayfirst=True)(self)

    @method
    class iter_investments(TableElement):
        head_xpath = '//table[@class="table-support"]/thead/tr/th'
        item_xpath = '//table[@class="table-support"]/tbody/tr'

        col_label = 'Supports'
        col_quantity = u'Quantité'
        col_unitvalue = 'Valeur'
        col_valuation = 'Evaluation'
        col_portfolio_share = u'%'

        class item(ItemElement):
            klass = Investment

            obj_label = CleanText(TableCell('label'))
            obj_quantity = MyDecimal(TableCell('quantity'))
            obj_unitvalue = MyDecimal(TableCell('unitvalue'))
            obj_valuation = MyDecimal(TableCell('valuation'))
            obj_portfolio_share = Eval(lambda x: x / 100, MyDecimal(TableCell('portfolio_share')))
            obj_code = NotAvailable
            obj_code_type = NotAvailable


class CardPage(AbstractAccountPage):
    def is_here(self):
        return bool(CleanText('//span[contains(., "Détail carte")]')(self.doc))

    def has_iban(self):
        return False

    def do_account_attachment(self, accounts):
        caccount_aid = Regexp(CleanText('//span[@id="C4__QUE_B160DC66D26AA39615599"]'), r'-(.*?)-')(self.doc)

        for account in accounts:
            if account.id == re.sub(r'\s', '', caccount_aid):
                return account

        return NotAvailable

    def has_history(self):
        return bool(self.doc.xpath('//h1[contains(@id, "C0B43C670D16A2667437")]/ancestor::node()[2][contains(@style, "display: none;")]'))

    @method
    class iter_history(TableElement):
        head_xpath = '//table[@class="table-cartes"]/thead/tr/th//a'
        item_xpath = '//table[@class="table-cartes"]/tbody/tr'

        col_label = u'Libellé'
        col_date = u'Date opération'

        class item(ItemElement):
            klass = Transaction

            def condition(self):
                tds = self.el.xpath('./td')
                if len(tds) == 1 and 'colspan' in tds[0].attrib:
                    assert self.page.doc.xpath('//h1[text()="Aucune opération"]')
                    return False
                return True

            obj_label = CleanText(TableCell('label'))
            obj_type = Transaction.TYPE_DEFERRED_CARD
            obj_date = Date(CleanText(TableCell('date')), dayfirst=True)

            def obj_amount(self):
                return MyDecimal('./td[5]//div/span')(self)


class IbanPDFPage(LoggedPage, PDFPage):
    def get_iban(self):
        match = re.search(r'Tm \[\((FR[0-9]{2} [A-Z0-9 ]+)\)\]', self.doc.decode('ISO8859-1'))

        if not match:
            return NotAvailable

        iban = match.group(1).replace(' ', '')

        assert is_iban_valid(iban)

        return iban
