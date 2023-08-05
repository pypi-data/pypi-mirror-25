# -*- coding: utf-8 -*-

# Copyright(C) 2013      Bezleputh
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
from datetime import datetime, time, timedelta

from weboob.browser.pages import HTMLPage, pagination
from weboob.browser.elements import ItemElement, ListElement, method
from weboob.browser.filters.standard import CleanText, Regexp, Filter, Env, BrowserURL, Format, DateTime
from weboob.browser.filters.html import CleanHTML
from weboob.capabilities.job import BaseJobAdvert
from weboob.capabilities.base import NotAvailable


class MonsterDate(Filter):
    def filter(self, date):
        now = datetime.now()
        number = re.search("\d+", date)
        if number:
            if 'heures' in date:
                date = now - timedelta(hours=int(number.group(0)))
                return datetime.combine(date, time())
            elif 'jour' in date:
                date = now - timedelta(days=int(number.group(0)))
                return datetime.combine(date, time())
        else:
            return datetime.combine(now, time.min)


class AdvSearchPage(HTMLPage):
    @pagination
    @method
    class iter_job_adverts(ListElement):
        item_xpath = '//article[@class="js_result_row"]'

        def next_page(self):
            page = Regexp(CleanText('//link[@rel="next"]/@href', default=''),
                          '.*page=(\d*)', default=None)(self)
            if page:
                return BrowserURL('adv_search', search=Env('search'), page=int(page))(self)

        class item(ItemElement):

            def condition(self):
                return u'Désolé' not in CleanText('//h1')(self)

            klass = BaseJobAdvert

            obj_id = CleanText('.//div[@class="jobTitle"]/h2/a/@data-m_impr_j_jobid')
            obj_society_name = CleanText('.//div[@class="company"]/span[@itemprop="name"]|.//div[@class="company"]/a/span[@itemprop="name"]',
                                         replace=[(u'Trouvée sur : ', u'')],
                                         default=NotAvailable)
            obj_title = CleanText('.//div[@class="jobTitle"]/h2/a/span',
                                  default=NotAvailable)
            obj_publication_date = DateTime(CleanText('.//div[has-class("job-specs-date")]/p/time/@datetime|./div[@class="extras"]/div[@class="postedDate"]/time/@datetime'),
                                            default=NotAvailable)
            obj_place = CleanText('.//div[has-class("job-specs-location")]|.//div[has-class("location")]',
                                  default=NotAvailable)


class AdvertPage(HTMLPage):
    @method
    class get_job_advert(ItemElement):
        klass = BaseJobAdvert

        obj_id = Env('_id')
        obj_url = BrowserURL('advert', _id=Env('_id'))
        obj_title = CleanText('//h2')
        obj_description = Format('%s\n%s',
                                 CleanHTML('//div[@id="JobDescription"]'),
                                 CleanText('//dl'))
        obj_contract_type = CleanText('(//dl/dt[text()="Type de contrat"]/following-sibling::dd)[1]')
        obj_society_name = CleanText('//div[@data-jsux="aboutCompany"]/div/dl/dd')
        obj_place = CleanText('//h3')
        obj_publication_date = MonsterDate(CleanText('(//dl/dt[starts-with(text(),"Publi")]/following-sibling::dd)[1]'))


class ExpiredAdvert(HTMLPage):
    @method
    class get_job_advert(ItemElement):
        klass = BaseJobAdvert

        obj_id = Env('_id')
        obj_url = BrowserURL('expired_advert', _id=Env('_id'))
        obj_title = CleanText('//div[@role="alert"]')
        obj_description = CleanText('//div[@role="alert"]')
