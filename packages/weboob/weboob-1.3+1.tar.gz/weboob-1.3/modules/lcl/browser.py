# -*- coding: utf-8 -*-

# Copyright(C) 2010-2012  Romain Bignon, Pierre Mazière
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


from datetime import datetime, timedelta
from functools import wraps

from weboob.exceptions import BrowserIncorrectPassword
from weboob.browser import LoginBrowser, URL, need_login, StatesMixin
from weboob.browser.exceptions import ServerError
from weboob.browser.pages import FormNotFound
from weboob.capabilities.base import NotAvailable
from weboob.capabilities.bank import Account, AddRecipientError, AddRecipientStep, Recipient
from weboob.tools.compat import basestring, urlsplit, parse_qsl, unicode
from weboob.tools.value import Value

from .pages import LoginPage, AccountsPage, AccountHistoryPage, \
                   CBListPage, CBHistoryPage, ContractsPage, ContractsChoicePage, BoursePage, \
                   AVPage, AVDetailPage, DiscPage, NoPermissionPage, RibPage, \
                   HomePage, LoansPage, TransferPage, AddRecipientPage, \
                   RecipientPage, RecipConfirmPage, SmsPage, RecipRecapPage, \
                   LoansProPage, Form2Page, DocumentsPage, ClientPage


__all__ = ['LCLBrowser','LCLProBrowser', 'ELCLBrowser']


# Browser
class LCLBrowser(LoginBrowser, StatesMixin):
    BASEURL = 'https://particuliers.secure.lcl.fr'
    STATE_DURATION = 15

    login = URL('/outil/UAUT/Authentication/authenticate',
                '/outil/UAUT\?from=.*',
                '/outil/UWER/Accueil/majicER',
                '/outil/UWER/Enregistrement/forwardAcc',
                LoginPage)
    contracts_page = URL('/outil/UAUT/Contrat/choixContrat.*',
                         '/outil/UAUT/Contract/getContract.*',
                         '/outil/UAUT/Contract/selectContracts.*',
                         '/outil/UAUT/Accueil/preRoutageLogin',
                         ContractsPage)
    contracts_choice = URL('.*outil/UAUT/Contract/routing', ContractsChoicePage)
    home = URL('/outil/UWHO/Accueil/', HomePage)
    accounts = URL('/outil/UWSP/Synthese', AccountsPage)
    client = URL('/outil/uwho', ClientPage)
    history = URL('/outil/UWLM/ListeMouvements.*/accesListeMouvements.*',
                  '/outil/UWLM/DetailMouvement.*/accesDetailMouvement.*',
                  '/outil/UWLM/Rebond',
                  AccountHistoryPage)
    rib = URL('/outil/UWRI/Accueil/detailRib',
              '/outil/UWRI/Accueil/listeRib', RibPage)
    finalrib = URL('/outil/UWRI/Accueil/', RibPage)
    cb_list = URL('/outil/UWCB/UWCBEncours.*/listeCBCompte.*', CBListPage)
    cb_history = URL('/outil/UWCB/UWCBEncours.*/listeOperations.*', CBHistoryPage)
    skip = URL('/outil/UAUT/Contrat/selectionnerContrat.*',
               '/index.html')
    no_perm = URL('/outil/UAUT/SansDroit/affichePageSansDroit.*', NoPermissionPage)

    bourse = URL('https://bourse.secure.lcl.fr/netfinca-titres/servlet/com.netfinca.frontcr.synthesis.HomeSynthesis',
                 'https://bourse.secure.lcl.fr/netfinca-titres/servlet/com.netfinca.frontcr.account.*',
                 '/outil/UWBO.*', BoursePage)
    disc = URL('https://bourse.secure.lcl.fr/netfinca-titres/servlet/com.netfinca.frontcr.login.ContextTransferDisconnect',
               r'https://assurance-vie-et-prevoyance.secure.lcl.fr/filiale/entreeBam\?.*\btypeaction=reroutage_retour\b',
               r'https://assurance-vie-et-prevoyance.secure.lcl.fr/filiale/ServletReroutageCookie',
               '/outil/UAUT/RetourPartenaire/retourCar', DiscPage)

    form2 = URL(r'/outil/UWVI/Routage/', Form2Page)

    assurancevie = URL('/outil/UWVI/AssuranceVie/accesSynthese',
                        '/outil/UWVI/AssuranceVie/accesDetail.*',
                        AVPage)
    avdetail = URL('https://assurance-vie-et-prevoyance.secure.lcl.fr.*', AVDetailPage)

    loans = URL('/outil/UWCR/SynthesePar/', LoansPage)
    loans_pro = URL('/outil/UWCR/SynthesePro/', LoansProPage)

    transfer_page = URL('/outil/UWVS/', TransferPage)
    confirm_transfer = URL('/outil/UWVS/Accueil/redirectView', TransferPage)
    recipients = URL('/outil/UWBE/Consultation/list', RecipientPage)
    add_recip = URL('/outil/UWBE/Creation/creationSaisie', AddRecipientPage)
    recip_confirm = URL('/outil/UWBE/Creation/creationConfirmation', RecipConfirmPage)
    send_sms = URL('/outil/UWBE/Otp/envoiCodeOtp\?telChoisi=MOBILE', '/outil/UWBE/Otp/getValidationCodeOtp\?codeOtp', SmsPage)
    recip_recap = URL('/outil/UWBE/Creation/executeCreation', RecipRecapPage)
    documents = URL('/outil/UWDM/ConsultationDocument/derniersReleves',
                    '/outil/UWDM/Recherche/afficherPlus',
                    '/outil/UWDM/Recherche/rechercherAll', DocumentsPage)

    __states__ = ('contracts', 'current_contract',)

    def __init__(self, *args, **kwargs):
        super(LCLBrowser, self).__init__(*args, **kwargs)
        self.accounts_list = None
        self.current_contract = None
        self.contracts = None

    def load_state(self, state):
        super(LCLBrowser, self).load_state(state)

        # lxml _ElementStringResult were put in the state, convert them to plain strs
        # TODO to remove at some point
        if self.contracts:
            self.contracts = [unicode(s) for s in self.contracts]
        if self.current_contract:
            self.current_contract = unicode(self.current_contract)

    def do_login(self):
        assert isinstance(self.username, basestring)
        assert isinstance(self.password, basestring)

        if not self.password.isdigit():
            raise BrowserIncorrectPassword()

        self.contracts = []
        self.current_contract = None

        # we force the browser to go to login page so it's work even
        # if the session expire
        self.login.go()

        if not self.page.login(self.username, self.password) or \
           (self.login.is_here() and self.page.is_error()) :
            raise BrowserIncorrectPassword("invalid login/password.\nIf you did not change anything, be sure to check for password renewal request on the original web site.")

        self.accounts_list = None
        self.accounts.stay_or_go()

    @need_login
    def connexion_bourse(self):
        self.location('/outil/UWBO/AccesBourse/temporisationCar?codeTicker=TICKERBOURSECLI')
        if self.no_perm.is_here():
            return False
        next_page = self.page.get_next()
        if next_page:
            self.location(self.page.get_next())
            self.bourse.stay_or_go()
            return True

    def deconnexion_bourse(self):
        self.disc.stay_or_go()

    def select_contract(self, id_contract):
        if self.current_contract and id_contract != self.current_contract:
            # when we go on bourse page, we can't change contract anymore... we have to logout.
            self.location('/outil/UAUT/Login/logout')
            # we already passed all checks on do_login so we consider it's ok.
            self.login.go().login(self.username, self.password)
            self.contracts_choice.go().select_contract(id_contract)

    def go_contract(f):
        @wraps(f)
        def wrapper(self, account, *args, **kwargs):
            self.select_contract(account._contract)
            return f(self, account, *args, **kwargs)
        return wrapper

    def check_accounts(self, account):
        return all(account.id != acc.id for acc in self.accounts_list)

    def update_accounts(self, account):
        if self.check_accounts(account):
            account._contract = self.current_contract
            self.accounts_list.append(account)

    @need_login
    def get_accounts(self):
        self.assurancevie.stay_or_go()
        # This is required in case the browser is left in the middle of add_recipient and the session expires.
        if self.login.is_here():
            return self.get_accounts_list()

        if self.accounts_list is None:
            self.accounts_list = []
        if self.no_perm.is_here():
            self.logger.warning('Life insurances are unavailable.')
        else:
            for a in self.page.get_list():
                self.update_accounts(a)
        self.accounts.stay_or_go()
        for a in self.page.get_list():
            if not self.check_accounts(a):
                continue
            self.location('/outil/UWRI/Accueil/')
            if self.page.has_iban_choice():
                self.rib.go(data={'compte': '%s/%s/%s' % (a.id[0:5], a.id[5:11], a.id[11:])})
                if self.rib.is_here():
                    iban = self.page.get_iban()
                    a.iban = iban if iban and a.id[11:] in iban else NotAvailable
            else:
                iban = self.page.check_iban_by_account(a.id)
                a.iban = iban if iban is not None else NotAvailable
            self.update_accounts(a)
        self.loans.stay_or_go()
        if self.no_perm.is_here():
            self.logger.warning('Loans are unavailable.')
        else:
            for a in self.page.get_list():
                self.update_accounts(a)
        self.loans_pro.stay_or_go()
        if self.no_perm.is_here():
            self.logger.warning('Loans are unavailable.')
        else:
            for a in self.page.get_list():
                self.update_accounts(a)
        if self.connexion_bourse():
            for a in self.page.get_list():
                self.update_accounts(a)
            self.deconnexion_bourse()
            # Disconnecting from bourse portal before returning account list
            # to be sure that we are on the banque portal

    @need_login
    def get_accounts_list(self):
        if self.accounts_list is None:
            if self.contracts and self.current_contract:
                for id_contract in self.contracts:
                    self.select_contract(id_contract)
                    self.get_accounts()
            else:
                self.get_accounts()
        return iter(self.accounts_list)

    @go_contract
    @need_login
    def get_history(self, account):
        if hasattr(account, '_market_link') and account._market_link:
            self.connexion_bourse()
            self.location(account._market_link)
            self.location(account._link_id).page.get_fullhistory()
            for tr in self.page.iter_history():
                yield tr
            self.deconnexion_bourse()
        elif hasattr(account, '_link_id') and account._link_id:
            try:
                self.location(account._link_id)
            except ServerError:
                return
            for tr in self.page.get_operations():
                yield tr
            for tr in self.get_cb_operations(account, 1):
                yield tr
        elif account.type == Account.TYPE_LIFE_INSURANCE and account._form:
            self.assurancevie.stay_or_go()
            account._form.submit()
            try:
                self.page.get_details(account, "OHIPU")
            except FormNotFound:
                assert self.page.is_restricted()
                self.logger.warning('restricted access to account %s', account)
            else:
                for tr in self.page.iter_history():
                    yield tr
            self.page.come_back()

    @go_contract
    @need_login
    def get_cb_operations(self, account, month=0):
        """
        Get CB operations.

        * month=0 : current operations (non debited)
        * month=1 : previous month operations (debited)
        """
        if not hasattr(account, '_coming_links'):
            return

        for link in account._coming_links:
            v = urlsplit(self.absurl(link))
            args = dict(parse_qsl(v.query))
            args['MOIS'] = month

            self.location(v.path, params=args)

            for tr in self.page.get_operations():
                yield tr

            for card_link in self.page.get_cards():
                self.location(card_link)
                for tr in self.page.get_operations():
                    yield tr

    @go_contract
    @need_login
    def get_investment(self, account):
        if account.type == Account.TYPE_LIFE_INSURANCE and account._form:
            self.assurancevie.stay_or_go()
            account._form.submit()
            if self.page.is_restricted():
                self.logger.warning('restricted access to account %s', account)
            else:
                for inv in self.page.iter_investment():
                    yield inv
            self.page.come_back()
        elif hasattr(account, '_market_link') and account._market_link:
            self.connexion_bourse()
            for inv in self.location(account._market_link).page.iter_investment():
                yield inv
            self.deconnexion_bourse()

    def locate_browser(self, state):
        if state['url'] == 'https://particuliers.secure.lcl.fr/outil/UWBE/Creation/creationConfirmation':
            self.logged = True
        else:
            super(LCLBrowser, self).locate_browser(state)

    @need_login
    def send_code(self, recipient, **params):
        res = self.open('/outil/UWBE/Otp/getValidationCodeOtp?codeOtp=%s' % params['code'])
        if res.text == 'false':
            raise AddRecipientError('Mauvais code sms.')
        self.recip_recap.go().check_values(recipient.iban, recipient.label)
        return self.get_recipient_object(recipient.iban, recipient.label)

    @need_login
    def get_recipient_object(self, iban, label):
        r = Recipient()
        r.iban = iban
        r.id = iban
        r.label = label
        r.category = u'Externe'
        r.enabled_at = datetime.now().replace(microsecond=0) + timedelta(days=5)
        r.currency = u'EUR'
        r.bank_name = NotAvailable
        return r

    @need_login
    def new_recipient(self, recipient, **params):
        if 'code' in params:
            return self.send_code(recipient, **params)
        try:
            assert recipient.iban[:2] in ['FR', 'MC']
        except AssertionError:
            raise AddRecipientError(u"LCL n'accepte que les iban commençant par MC ou FR.")
        for _ in range(2):
            self.add_recip.go()
            if self.add_recip.is_here():
                break
        try:
            assert self.add_recip.is_here()
        except AssertionError:
            raise AddRecipientError('Navigation failed: not on add_recip.')
        self.page.validate(recipient.iban, recipient.label)
        try:
            assert self.recip_confirm.is_here()
        except AssertionError:
            raise AddRecipientError('Navigation failed: not on recip_confirm.')
        self.page.check_values(recipient.iban, recipient.label)
        # Send sms to user.
        self.open('/outil/UWBE/Otp/envoiCodeOtp?telChoisi=MOBILE')
        raise AddRecipientStep(self.get_recipient_object(recipient.iban, recipient.label), Value('code', label='Saisissez le code.'))

    @go_contract
    @need_login
    def iter_recipients(self, origin_account):
        if origin_account._transfer_id is None:
            return
        self.transfer_page.go()
        if self.no_perm.is_here() or not self.page.can_transfer(origin_account._transfer_id):
            return
        self.page.choose_origin(origin_account._transfer_id)
        for recipient in self.page.iter_recipients(account_transfer_id=origin_account._transfer_id):
            yield recipient

    @go_contract
    @need_login
    def init_transfer(self, account, recipient, amount, reason=None):
        self.transfer_page.go()
        self.page.choose_origin(account._transfer_id)
        self.page.choose_recip(recipient)
        self.page.transfer(amount, reason)
        self.page.check_data_consistency(account, recipient, amount, reason)
        return self.page.create_transfer(account, recipient, amount, reason)

    @need_login
    def execute_transfer(self, transfer):
        self.page.confirm()
        return self.page.fill_transfer_id(transfer)

    @need_login
    def get_advisor(self):
        return iter([self.accounts.stay_or_go().get_advisor()])

    @need_login
    def iter_subscriptions(self):
        yield self.client.go().get_item()

    @need_login
    def iter_documents(self, subscription):
        documents = []
        self.documents.go()
        self.location('https://particuliers.secure.lcl.fr/outil/UWDM/Recherche/afficherPlus')
        self.page.do_search_request()
        for document in self.page.get_list():
            documents.append(document)
        return documents


class LCLProBrowser(LCLBrowser):
    BASEURL = 'https://professionnels.secure.lcl.fr'

    #We need to add this on the login form
    IDENTIFIANT_ROUTING = 'CLA'

    def __init__(self, *args, **kwargs):
        super(LCLProBrowser, self).__init__(*args, **kwargs)
        self.session.cookies.set("lclgen","professionnels")


class ELCLBrowser(LCLBrowser):
    BASEURL = 'https://e.secure.lcl.fr'

    IDENTIFIANT_ROUTING = 'ELCL'

    def __init__(self, *args, **kwargs):
        super(ELCLBrowser, self).__init__(*args, **kwargs)

        self.session.cookies.set('lclgen', 'ecl')
