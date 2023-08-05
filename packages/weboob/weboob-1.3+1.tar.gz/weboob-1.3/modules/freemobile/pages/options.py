# -*- coding: utf-8 -*-

# Copyright(C) 2012-2014 Florent Fourcot
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


from weboob.browser.pages import LoggedPage

from .history import BadUTF8Page


class OptionsPage(LoggedPage, BadUTF8Page):
    def get_api_key(self):
        api_key = self.doc.xpath(
            '//div[contains(@class, "div_gestionOptions")]//span[contains(@class, "secret-key")]'
        )
        if api_key:
            return api_key[0].text.strip()
        else:
            return None
