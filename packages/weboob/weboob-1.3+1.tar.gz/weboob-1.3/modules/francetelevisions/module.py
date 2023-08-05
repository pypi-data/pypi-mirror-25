# -*- coding: utf-8 -*-

# Copyright(C) 2011  Romain Bignon
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

from weboob.capabilities.base import find_object
from weboob.capabilities.video import CapVideo, BaseVideo
from weboob.capabilities.collection import CapCollection, CollectionNotFound
from weboob.tools.backend import Module

from .browser import PluzzBrowser


__all__ = ['PluzzModule']


class PluzzModule(Module, CapVideo, CapCollection):
    NAME = 'francetelevisions'
    MAINTAINER = u'Romain Bignon'
    EMAIL = 'romain@weboob.org'
    VERSION = '1.3'
    DESCRIPTION = u'France Télévisions video website'
    LICENSE = 'AGPLv3+'
    BROWSER = PluzzBrowser

    def get_video(self, _id):
        return self.browser.get_video(_id)

    def search_videos(self, pattern, sortby=CapVideo.SEARCH_RELEVANCE, nsfw=False):
        return self.browser.search_videos(pattern)

    def fill_video(self, video, fields):
        if 'url' in fields:
            video = self.browser.get_video(video.id)
        if 'thumbnail' in fields and video.thumbnail:
            video.thumbnail.data = self.browser.open(video.thumbnail.url).content
        return video

    def iter_resources(self, objs, split_path):
        if BaseVideo in objs:
            collection = self.get_collection(objs, split_path)
            if collection.path_level == 0:
                for category in self.browser.get_categories():
                    yield category
            elif collection.path_level == 1 and collection.split_path[0].startswith('vid_'):
                cat = find_object(self.browser.get_categories(), id=collection.split_path[0], error=None)
                for video in self.browser.iter_videos(cat.title):
                    yield video
            else:
                for cat in self.browser.iter_subcategories(collection.split_path):
                    yield cat

    def validate_collection(self, objs, collection):
        if collection.path_level <= 2:
            return

        raise CollectionNotFound(collection.split_path)

    OBJECTS = {BaseVideo: fill_video}
