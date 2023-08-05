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

from decimal import Decimal
import re
import requests
import ast

from weboob.browser.pages import HTMLPage, pagination, LoggedPage
from weboob.browser.elements import method, TableElement, ItemElement
from weboob.browser.filters.standard import Env, CleanDecimal, CleanText, TableCell, Date, Regexp, Eval, Field
from weboob.browser.filters.html import Attr, Link
from weboob.browser.filters.javascript import JSVar
from weboob.capabilities.bank import Account, Investment
from weboob.capabilities.base import NotAvailable
from weboob.tools.capabilities.bank.transactions import FrenchTransaction


class LoginPage(HTMLPage):
    def login(self, login, passwd):
        tab = re.search(r'tab = (\[[\d,\s]*\])', self.content).group(1)
        number_list = ast.literal_eval(tab)
        key_map = {}
        for i, number in enumerate(number_list):
            if number < 10:
                key_map[number] = chr(ord('A') + i)
        pass_string = ''.join(key_map[int(n)] for n in passwd)
        form = self.get_form(name='loginForm')
        form['username'] = login
        form['password'] = pass_string
        form.submit()


class AccountsPage(HTMLPage):
    logged = True
    ACCOUNT_TYPES = {u'Solde des comptes bancaires - Groupama Banque':  Account.TYPE_CHECKING,
                     u'Solde des comptes bancaires': Account.TYPE_CHECKING,
                     u'Epargne bancaire constituée - Groupama Banque':  Account.TYPE_SAVINGS,
                     u'Epargne bancaire constituée':  Account.TYPE_SAVINGS,
                     u'Assurance Vie':  Account.TYPE_LIFE_INSURANCE,
                    }

    def get_list(self):
        account_type = Account.TYPE_UNKNOWN
        accounts = []

        for tr in self.doc.xpath('//div[@class="finance"]/form/table[@class="ecli"]/tr'):
            if tr.attrib.get('class', '') == 'entete':
                account_type = self.ACCOUNT_TYPES.get(tr.find('th').text.strip(), Account.TYPE_UNKNOWN)
                continue

            tds = tr.findall('td')
            a = tds[0].find('a')

            # Skip accounts that can't be accessed
            if a is None:
                continue

            balance = tds[-1].text.strip()

            account = Account()
            account.label = u' '.join([txt.strip() for txt in tds[0].itertext()])
            account.label = re.sub(u'[ \xa0\u2022\r\n\t]+', u' ', account.label).strip()
            account.id = Regexp(pattern=u'N° ((.*?) |(.*))').filter(account.label).strip()
            account.type = account_type
            if balance:
                account.balance = Decimal(FrenchTransaction.clean_amount(balance))
                account.currency = account.get_currency(balance)

            if 'onclick' in a.attrib:
                m = re.search(r"javascript:submitForm\(([\w_]+),'([^']+)'\);", a.attrib['onclick'])
                if not m:
                    self.logger.warning('Unable to find link for %r' % account.label)
                    account._link = None
                else:
                    account._link = m.group(2)
            else:
                account._link = a.attrib['href'].strip()

            accounts.append(account)

        return accounts


class Transaction(FrenchTransaction):
    PATTERNS = [(re.compile('^Facture (?P<dd>\d{2})/(?P<mm>\d{2})-(?P<text>.*) carte .*'),
                                                                FrenchTransaction.TYPE_CARD),
                (re.compile(u'^(Prlv( de)?|Ech(éance|\.)) (?P<text>.*)'),
                                                                FrenchTransaction.TYPE_ORDER),
                (re.compile('^(Vir|VIR)( de)? (?P<text>.*)'),
                                                                FrenchTransaction.TYPE_TRANSFER),
                (re.compile(u'^CHEQUE.*? (N° \w+)?$'),          FrenchTransaction.TYPE_CHECK),
                (re.compile('^Cotis(ation)? (?P<text>.*)'),
                                                                FrenchTransaction.TYPE_BANK),
                (re.compile('(?P<text>Int .*)'),                FrenchTransaction.TYPE_BANK),
               ]


class TransactionsPage(HTMLPage):
    logged = True

    @pagination
    @method
    class get_history(Transaction.TransactionsElement):
        head_xpath = '//table[@id="releve_operation"]//tr/th'
        item_xpath = '//table[@id="releve_operation"]//tr'

        col_date =       [u'Date opé', 'Date', u'Date d\'opé', u'Date opération']
        col_vdate =      [u'Date valeur']
        col_credit =     [u'Crédit', u'Montant', u'Valeur']
        col_debit =      [u'Débit']

        def next_page(self):
            url = Attr('//a[contains(text(), "Page suivante")]', 'onclick', default=None)(self)
            if url:
                m = re.search('\'([^\']+).*([\d]+)', url)
                return requests.Request("POST", m.group(1), data={'numCompte': Env('accid')(self), \
                                        'vue': "ReleveOperations", 'tri': "DateOperation", 'sens': \
                                        "DESC", 'page': m.group(2), 'nb_element': "25"})

        class item(Transaction.TransactionElement):
            def condition(self):
                return len(self.el.xpath('./td')) > 3

    def get_coming_link(self):
        try:
            a = self.doc.getroot().cssselect('div#sous_nav ul li a.bt_sans_off')[0]
        except IndexError:
            return None
        return re.sub('[ \t\r\n]+', '', a.attrib['href'])


class AVAccountPage(LoggedPage, HTMLPage):
    """
    Get balance

    :return: decimal balance, currency
    :rtype: tuple
    """
    def get_av_balance(self):
        balance_xpath = u'//p[contains(text(), "Épargne constituée")]/span'

        return (CleanDecimal(balance_xpath)(self.doc), Account.get_currency(CleanText(balance_xpath)(self.doc)))

    @method
    class get_av_investments(TableElement):
        item_xpath = '//table[@id="repartition_epargne3"]/tr[position() > 1]'
        head_xpath = '//table[@id="repartition_epargne3"]/tr/th[position() > 1]'

        col_quantity = u'Nombre d’unités de compte'
        col_unitvalue = u"Valeur de l’unité de compte"
        col_valuation = u'Épargne constituée en euros'
        col_portfolio_share = u'Répartition %'

        class item(ItemElement):
            klass = Investment

            def condition(self):
                return Field('quantity')(self) is not NotAvailable

            obj_label = CleanText('./th')
            obj_quantity = CleanDecimal(TableCell('quantity'), default=NotAvailable)
            obj_unitvalue = CleanDecimal(TableCell('unitvalue'))
            obj_valuation = CleanDecimal(TableCell('valuation'))
            obj_portfolio_share = Eval(lambda x: x / 100, CleanDecimal(TableCell('portfolio_share')))
            obj_code = Regexp(Link('./th/a'), r'isin=(\w+)|/(\w+)\.pdf')
            obj_code_type = Investment.CODE_TYPE_ISIN


class AVHistoryPage(LoggedPage, HTMLPage):
    @method
    class get_av_history(TableElement):
        item_xpath = '//table[@id="enteteTableSupports"]/tbody/tr'
        head_xpath = '//table[@id="enteteTableSupports"]/thead/tr/th'

        col_date = 'Date'
        col_label = 'Type de mouvement'
        col_debit = u'Montant Désinvesti'
        col_credit = ['Montant investi', u'Montant Net Perçu']
        # There is several types of life insurances, so multiple columns
        col_credit2 = [u'Montant Brut Versé']

        class item(ItemElement):
            klass = Transaction

            def condition(self):
                return CleanText(TableCell('date'))(self) != 'en cours'

            obj_label = CleanText(TableCell('label'))
            obj_type = Transaction.TYPE_BANK
            obj_date = Date(CleanText(TableCell('date')), dayfirst=True)
            obj__arbitration = False

            def obj_amount(self):
                credit = CleanDecimal(TableCell('credit'), default=Decimal(0))(self)
                # Different types of life insurances, use different columns.
                if TableCell('debit', default=None)(self):
                    debit = CleanDecimal(TableCell('debit'), default=Decimal(0))(self)
                    # In case of financial arbitration, both columns are equal
                    if credit and debit:
                        assert credit == debit
                        self.obj._arbitration = True
                        return credit
                    else:
                        return credit - abs(debit)
                else:
                    credit2 = CleanDecimal(TableCell('credit2'), default=Decimal(0))(self)
                    assert not (credit and credit2)
                    return credit + credit2


class FormPage(LoggedPage, HTMLPage):
    def av_account_form(self):
        form = self.get_form('//form[@id="formGoToRivage"]')
        form['gfr_numeroContrat'] = JSVar(var='numContrat').filter(CleanText('//script[contains(text(), "var numContrat")]')(self.doc))
        form['gfr_data'] = JSVar(var='pCryptage').filter(CleanText('//script[contains(text(), "var pCryptage")]')(self.doc))
        form['gfr_adrSite'] = 'https://espaceclient.%s.fr' % self.browser.website
        form.url = 'https://secure-rivage.%s.fr/contratVie.rivage.syntheseContratEparUc.gsi' % self.browser.website
        form.submit()
