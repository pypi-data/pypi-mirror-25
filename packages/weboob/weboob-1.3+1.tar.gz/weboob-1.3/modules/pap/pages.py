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

from weboob.tools.date import parse_french_date
from weboob.browser.pages import HTMLPage, JsonPage, pagination
from weboob.browser.elements import ItemElement, ListElement, DictElement, method
from weboob.browser.filters.standard import CleanText, CleanDecimal, Regexp, Env, BrowserURL, Format
from weboob.browser.filters.html import Attr, Link, XPath, CleanHTML
from weboob.browser.filters.json import Dict
from weboob.capabilities.base import NotAvailable
from weboob.capabilities.housing import Housing, City, HousingPhoto, UTILITIES
from weboob.tools.capabilities.housing.housing import PricePerMeterFilter


class CitiesPage(JsonPage):
    @method
    class iter_cities(DictElement):

        class item(ItemElement):
            klass = City

            obj_id = Dict('id')
            obj_name = Dict('name')


class SearchResultsPage(HTMLPage):
    @pagination
    @method
    class iter_housings(ListElement):
        item_xpath = '//div[has-class("search-results-item")]'

        def next_page(self):
            return Link('//ul[@class="pagination"]/li[@class="next"]/a')(self)

        class item(ItemElement):
            klass = Housing

            def condition(self):
                return Regexp(Link('./div[has-class("box-header")]/a[@class="title-item"]'), '/annonces/(.*)', default=None)(self)

            obj_id = Regexp(Link('./div[has-class("box-header")]/a[@class="title-item"]'), '/annonces/(.*)')
            obj_title = CleanText('./div[has-class("box-header")]/a[@class="title-item"]')
            obj_area = CleanDecimal(Regexp(CleanText('./div[has-class("box-header")]/a/span[@class="h1"]'),
                                           '(.*?)(\d*) m\xb2(.*?)', '\\2'), default=NotAvailable)
            obj_cost = CleanDecimal(CleanText('./div[has-class("box-header")]/a/span[@class="price"]'),
                                    replace_dots=True, default=Decimal(0))
            obj_currency = Regexp(CleanText('./div[has-class("box-header")]/a/span[@class="price"]'),
                                  '.*([%s%s%s])' % (u'€', u'$', u'£'), default=u'€')
            obj_utilities = UTILITIES.UNKNOWN

            def obj_date(self):
                _date = Regexp(CleanText('./div[has-class("box-header")]/p[@class="date"]'),
                               '.* / (.*)')(self)
                return parse_french_date(_date)

            obj_station = CleanText('./div[@class="box-body"]/div/div/p[@class="item-transports"]', default=NotAvailable)
            obj_location = CleanText('./div[@class="box-body"]/div/div/p[@class="item-description"]/strong')
            obj_text = CleanText('./div[@class="box-body"]/div/div/p[@class="item-description"]')
            obj_rooms = CleanDecimal(
                './div[@class="box-body"]/div/div/div[@class="clearfix"]/ul[has-class("item-summary")]/li[1]/strong',
                default=NotAvailable
            )
            obj_price_per_meter = PricePerMeterFilter()

            def obj_bedrooms(self):
                rooms_bedrooms_area = XPath(
                    './div[@class="box-body"]/div/div/div[@class="clearfix"]/ul[has-class("item-summary")]/li'
                )(self)
                if len(rooms_bedrooms_area) > 2:
                    return CleanDecimal(
                        './div[@class="box-body"]/div/div/div[@class="clearfix"]/ul[has-class("item-summary")]/li[2]/strong',
                        default=NotAvailable
                    )(self)
                else:
                    return NotAvailable

            obj_url = Format(
                u'http://www.pap.fr%s',
                Link(
                    './div[@class="box-body"]/div/div/div[@class="clearfix"]/div[@class="float-right"]/a'
                )
            )

            def obj_photos(self):
                photos = []
                for img in XPath('./div[@class="box-body"]/div/div/a/img/@src')(self):
                    photos.append(HousingPhoto(u'%s' % img))
                return photos


class HousingPage(HTMLPage):
    @method
    class get_housing(ItemElement):
        klass = Housing

        obj_id = Env('_id')
        obj_title = CleanText(
            '//div[has-class("box-header")]/h1[@class="clearfix"]'
        )
        obj_cost = CleanDecimal('//h1[@class="clearfix"]/span[@class="price"]',
                                replace_dots=True)
        obj_currency = Regexp(CleanText('//h1[@class="clearfix"]/span[@class="price"]'),
                              '.*([%s%s%s])' % (u'€', u'$', u'£'), default=u'€')
        obj_utilities = UTILITIES.UNKNOWN
        obj_area = CleanDecimal(Regexp(CleanText('//h1[@class="clearfix"]/span[@class="title"]'),
                                '(.*?)(\d*) m\xb2(.*?)', '\\2'), default=NotAvailable)

        def obj_date(self):
            date = CleanText(
                '//div[has-class("box-header")]//p[has-class("date")]'
            )(self).split("/")[-1].strip()
            return parse_french_date(date)

        def obj_bedrooms(self):
            rooms_bedrooms_area = XPath(
                '//div[has-class("box-body")]//ul[has-class("item-summary")]/li'
            )(self)
            if len(rooms_bedrooms_area) > 2:
                return CleanDecimal(
                    '//div[has-class("box-body")]//ul[has-class("item-summary")]/li[2]/strong',
                    default=NotAvailable
                )(self)
            else:
                return NotAvailable

        obj_rooms = CleanText('//ul[has-class("item-summary")]/li[1]/strong',
                              default=NotAvailable)
        obj_price_per_meter = PricePerMeterFilter()
        obj_location = CleanText('//div[@class="item-geoloc"]/h2')
        obj_text = CleanText(CleanHTML('//p[@class="item-description"]'))

        def obj_station(self):
            return ", ".join([
                station.text
                for station in XPath(
                    '//ul[has-class("item-metro")]//span[has-class("label")]'
                )(self)
            ])

        def obj_phone(self):
            phone = CleanText('(//div[has-class("tel-wrapper")])[1]')(self)
            phone = phone.replace(' ', ', ')
            return phone.strip()

        obj_url = BrowserURL('housing', _id=Env('_id'))

        def obj_details(self):
            GES = Attr(
                '//div[has-class("energy-box")]//div[has-class("rank")]',
                'class',
                default=None
            )(self)
            if GES:
                GES = [x.replace("rank-", "").upper()
                       for x in GES.split() if x.startswith("rank-")][0]
            else:
                GES = NotAvailable
            return {
                "GES": GES
            }

        def obj_photos(self):
            photos = []
            for img in XPath('//div[has-class("owl-carousel-thumbs")]//img/@src')(self):
                photos.append(HousingPhoto(u'%s' % img))
            return photos
