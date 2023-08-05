# -*- coding: utf-8 -*-

# Copyright(C) 2012 Arno Renevier
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


from weboob.browser import PagesBrowser, URL
from .pages import WeatherPage, CityPage

__all__ = ['WeatherBrowser']


class WeatherBrowser(PagesBrowser):
    BASEURL = 'https://www.weather.com'
    API_KEY = 'c1ea9f47f6a88b9acb43aba7faf389d4'

    city_page = URL('https://dsx\.weather\.com/x/v2/web/loc/fr_FR/1/4/5/9/11/13/19/21/1000/1001/1003/fr%5E/\((?P<pattern>.*)\)', CityPage)

    weather_page = URL('https://api\.weather\.com/v2/turbo/vt1currentdatetime;vt1observation\?units=m&language=fr-FR&geocode=(?P<city_id>.*)&format=json&apiKey=(?P<api>.*)',
                       WeatherPage)

    forecast_page = URL('https://api\.weather\.com/v2/turbo/vt1dailyForecast\?units=m&language=fr-FR&geocode=(?P<city_id>.*)&format=json&apiKey=(?P<api>.*)',
                        WeatherPage)

    def iter_city_search(self, pattern):
        return self.city_page.go(pattern=pattern).iter_cities()

    def get_current(self, city_id):
        return self.weather_page.go(city_id=city_id, api=self.API_KEY).get_current()

    def iter_forecast(self, city_id):
        return self.forecast_page.go(city_id=city_id, api=self.API_KEY).iter_forecast()
