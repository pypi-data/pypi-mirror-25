# Author: Mr_Orange
# URL: https://sickrage.ca
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import re
import urllib

import sickrage
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.helpers import convert_size
from sickrage.providers import TorrentProvider


class NyaaProvider(TorrentProvider):
    def __init__(self):
        super(NyaaProvider, self).__init__("NyaaTorrents", 'http://nyaa.si', False)

        self.supports_backlog = True

        self.supports_absolute_numbering = True
        self.anime_only = True
        self.ratio = None

        self.cache = TVCache(self, min_time=15)

        self.minseed = 0
        self.minleech = 0
        self.confirmed = False

    def search(self, search_strings, search_mode='eponly', epcount=0, age=0, epObj=None):
        if self.show and not self.show.is_anime:
            return []

        results = []
        items = {'Season': [], 'Episode': [], 'RSS': []}

        for mode in search_strings.keys():
            sickrage.srCore.srLogger.debug("Search Mode: %s" % mode)
            for search_string in search_strings[mode]:
                if mode != 'RSS':
                    sickrage.srCore.srLogger.debug("Search string: %s" % search_string)

                params = {
                    "page": 'rss',
                    "cats": '1_0',  # All anime
                    "sort": 2,  # Sort Descending By Seeders
                    "order": 1
                }
                if mode != 'RSS':
                    params["term"] = search_string.encode('utf-8')

                searchURL = self.urls['base_url'] + '?' + urllib.urlencode(params)
                sickrage.srCore.srLogger.debug("Search URL: %s" % searchURL)

                summary_regex = ur"(\d+) seeder\(s\), (\d+) leecher\(s\), \d+ download\(s\) - (\d+.?\d* [KMGT]iB)(.*)"
                s = re.compile(summary_regex, re.DOTALL)

                results = []
                for curItem in self.cache.getRSSFeed(searchURL)['entries'] or []:
                    title = curItem['title']
                    download_url = curItem['link']
                    if not all([title, download_url]):
                        continue

                    seeders, leechers, size, verified = s.findall(curItem['summary'])[0]
                    size = convert_size(size)

                    # Filter unseeded torrent
                    if seeders < self.minseed or leechers < self.minleech:
                        if mode != 'RSS':
                            sickrage.srCore.srLogger.debug(
                                "Discarding torrent because it doesn't meet the minimum seeders or leechers: {} (S:{} L:{})".format(
                                    title, seeders, leechers))
                        continue

                    if self.confirmed and not verified and mode != 'RSS':
                        sickrage.srCore.srLogger.debug(
                            "Found result " + title + " but that doesn't seem like a verified result so I'm ignoring it")
                        continue

                    item = title, download_url, size, seeders, leechers
                    if mode != 'RSS':
                        sickrage.srCore.srLogger.debug("Found result: %s " % title)

                    items[mode].append(item)

            # For each search mode sort all the items by seeders if available
            items[mode].sort(key=lambda tup: tup[3], reverse=True)

            results += items[mode]

        return results

    def seed_ratio(self):
        return self.ratio
