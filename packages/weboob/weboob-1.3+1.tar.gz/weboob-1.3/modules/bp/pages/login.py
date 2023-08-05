# -*- coding: utf-8 -*-

# Copyright(C) 2010-2011 Nicolas Duhamel
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

from __future__ import unicode_literals, division

from io import BytesIO

from weboob.exceptions import BrowserUnavailable, BrowserIncorrectPassword, NoAccountsException
from weboob.browser.pages import LoggedPage
from weboob.browser.filters.standard import CleanText, Regexp
from weboob.tools.captcha.virtkeyboard import VirtKeyboard

from .base import MyHTMLPage


class UnavailablePage(MyHTMLPage):
    def on_load(self):
        raise BrowserUnavailable()


class Keyboard(VirtKeyboard):
    symbols={'0':'daa52d75287bea58f505823ef6c8b96c',
             '1':'f5da96c2592803a8cdc5a928a2e4a3b0',
             '2':'9ff78367d5cb89cacae475368a11e3af',
             '3':'908a0a42a424b95d4d885ce91bc3d920',
             '4':'3fc069f33b801b3d0cdce6655a65c0ac',
             '5':'58a2afebf1551d45ccad79fad1600fc3',
             '6':'7fedfd9e57007f2985c3a1f44fb38ea1',
             '7':'389b8ef432ae996ac0141a2fcc7b540f',
             '8':'bf357ff09cc29ea544991642cd97d453',
             '9':'b744015eb89c1b950e13a81364112cd6',
            }

    color=(0xff, 0xff, 0xff)

    def __init__(self, page):
        img_url = Regexp(CleanText('//style'), r'background:url\((.*?)\)', default=None)(page.doc) or \
                  Regexp(CleanText('//script'), r'IMG_ALL = "(.*?)"', default=None)(page.doc)
        size = 252
        if not img_url:
            img_url = page.doc.xpath('//img[@id="imageCVS"]')[0].attrib['src']
            size = 146
        coords = {}

        x, y, width, height = (0, 0, size // 4, size // 4)
        for i, _ in enumerate(page.doc.xpath('//div[@id="imageclavier"]//button')):
            code = '%02d' % i
            coords[code] = (x+4, y+4, x+width-8, y+height-8)
            if (x + width + 1) >= size:
                y += height + 1
                x = 0
            else:
                x += width + 1

        data = page.browser.open(img_url).content
        VirtKeyboard.__init__(self, BytesIO(data), coords, self.color)

        self.check_symbols(self.symbols, page.browser.responses_dirname)

    def get_symbol_code(self,md5sum):
        code = VirtKeyboard.get_symbol_code(self,md5sum)
        return '%02d' % int(code.split('_')[-1])

    def get_string_code(self,string):
        code = ''
        for c in string:
            code += self.get_symbol_code(self.symbols[c])
        return code

    def get_symbol_coords(self, coords):
        # strip borders
        x1, y1, x2, y2 = coords
        return VirtKeyboard.get_symbol_coords(self, (x1+3, y1+3, x2-3, y2-3))


class LoginPage(MyHTMLPage):
    def login(self, login, pwd):
        vk = Keyboard(self)

        form = self.get_form(name='formAccesCompte')
        form['password'] = vk.get_string_code(pwd)
        form['username'] = login.encode(self.ENCODING)
        form.submit()


class repositionnerCheminCourant(LoggedPage, MyHTMLPage):
    def on_load(self):
        super(repositionnerCheminCourant, self).on_load()
        response = self.browser.open("https://voscomptesenligne.labanquepostale.fr/voscomptes/canalXHTML/securite/authentification/initialiser-identif.ea")
        if isinstance(response.page, Initident):
            response.page.on_load()
        if "vous ne disposez pas" in response.text:
            raise BrowserIncorrectPassword("No online banking service for these ids")
        if 'Nous vous invitons à renouveler votre opération ultérieurement' in response.text:
            raise BrowserUnavailable()


class Initident(LoggedPage, MyHTMLPage):
    def on_load(self):
        self.browser.open("https://voscomptesenligne.labanquepostale.fr/voscomptes/canalXHTML/securite/authentification/verifierMotDePasse-identif.ea")
        if self.doc.xpath(u'//span[contains(text(), "L\'identifiant utilisé est celui d\'une Entreprise ou d\'une Association")]'):
            raise BrowserIncorrectPassword(u"L'identifiant utilisé est celui d'une Entreprise ou d'une Association")
        no_accounts = CleanText(u'//div[@class="textFCK"]')(self.doc)
        if no_accounts:
            raise NoAccountsException(no_accounts)
        MyHTMLPage.on_load(self)


class CheckPassword(LoggedPage, MyHTMLPage):
    def on_load(self):
        MyHTMLPage.on_load(self)
        self.browser.location("https://voscomptesenligne.labanquepostale.fr/voscomptes/canalXHTML/comptesCommun/synthese_assurancesEtComptes/init-synthese.ea")


class BadLoginPage(MyHTMLPage):
    pass


class AccountDesactivate(LoggedPage, MyHTMLPage):
    pass
