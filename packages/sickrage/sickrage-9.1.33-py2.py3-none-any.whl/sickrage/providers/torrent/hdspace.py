# Author: Idan Gutman
# Modified by jkaberg, https://github.com/jkaberg for SceneAccess
# Modified by 7ca for HDSpace
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
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import re
import urllib

import requests

import sickrage
from sickrage.core.caches.tv_cache import TVCache
from sickrage.core.helpers import bs4_parser, convert_size
from sickrage.providers import TorrentProvider


class HDSpaceProvider(TorrentProvider):
    def __init__(self):
        super(HDSpaceProvider, self).__init__("HDSpace", 'http://hd-space.org', True)

        self.supports_backlog = True

        self.username = None
        self.password = None
        self.ratio = None
        self.minseed = None
        self.minleech = None

        self.cache = TVCache(self, min_time=10)

        self.urls.update({
            'login': '{base_url}/index.php?page=login'.format(base_url=self.urls['base_url']),
            'search': '{base_url}/index.php?page=torrents&search=%s&active=1&options=0&category='.format(
                base_url=self.urls['base_url']),
            'rss': '{base_url}/rss_torrents.php?feed=dl'.format(base_url=self.urls['base_url'])
        })

        self.categories = [15, 21, 22, 24, 25, 40]  # HDTV/DOC 1080/720, bluray, remux
        for cat in self.categories:
            self.urls['search'] += str(cat) + '%%3B'
            self.urls['rss'] += '&cat[]=' + str(cat)
        self.urls['search'] = self.urls['search'][:-4]  # remove extra %%3B

    def _check_auth(self):

        if not self.username or not self.password:
            sickrage.srCore.srLogger.warning(
                "[{}]: Invalid username or password. Check your settings".format(self.name))

        return True

    def login(self):

        if 'pass' in requests.utils.dict_from_cookiejar(sickrage.srCore.srWebSession.cookies):
            return True

        login_params = {'uid': self.username,
                        'pwd': self.password}

        try:
            response = sickrage.srCore.srWebSession.post(self.urls['login'], data=login_params, timeout=30).text
        except Exception:
            sickrage.srCore.srLogger.warning("[{}]: Unable to connect to provider".format(self.name))
            return False

        if re.search('Password Incorrect', response):
            sickrage.srCore.srLogger.warning(
                "[{}]: Invalid username or password. Check your settings".format(self.name))
            return False

        return True

    def search(self, search_strings, search_mode='eponly', epcount=0, age=0, epObj=None):

        results = []
        items = {'Season': [], 'Episode': [], 'RSS': []}

        if not self.login():
            return results

        for mode in search_strings.keys():
            sickrage.srCore.srLogger.debug("Search Mode: %s" % mode)
            for search_string in search_strings[mode]:

                if mode != 'RSS':
                    searchURL = self.urls['search'] % (urllib.quote_plus(search_string.replace('.', ' ')),)
                else:
                    searchURL = self.urls['search'] % ''

                sickrage.srCore.srLogger.debug("Search URL: %s" % searchURL)
                if mode != 'RSS':
                    sickrage.srCore.srLogger.debug("Search string: %s" % search_string)

                try:
                    data = sickrage.srCore.srWebSession.get(searchURL, cache=False).text
                except Exception:
                    sickrage.srCore.srLogger.debug("No data returned from provider")
                    continue

                # Search result page contains some invalid html that prevents html parser from returning all data.
                # We cut everything before the table that contains the data we are interested in thus eliminating
                # the invalid html portions
                try:
                    data = data.split('<div id="information"></div>')[1]
                    index = data.index('<table')
                except ValueError:
                    sickrage.srCore.srLogger.error("Could not find main torrent table")
                    continue

                with bs4_parser(data[index:]) as html:
                    if not html:
                        sickrage.srCore.srLogger.debug("No html data parsed from provider")
                        continue

                torrents = html.findAll('tr')
                if not torrents:
                    continue

                # Skip column headers
                for result in torrents[1:]:
                    if len(result.contents) < 10:
                        # skip extraneous rows at the end
                        continue

                    try:
                        dl_href = result.find('a', attrs={'href': re.compile(r'download.php.*')})['href']
                        title = re.search('f=(.*).torrent', dl_href).group(1).replace('+', '.')
                        download_url = self.urls['base_url'] + dl_href
                        seeders = int(result.find('span', attrs={'class': 'seedy'}).find('a').text)
                        leechers = int(result.find('span', attrs={'class': 'leechy'}).find('a').text)
                        size = convert_size(result)

                        if not all([title, download_url]):
                            continue

                        # Filter unseeded torrent
                        if seeders < self.minseed or leechers < self.minleech:
                            if mode != 'RSS':
                                sickrage.srCore.srLogger.debug(
                                    "Discarding torrent because it doesn't meet the minimum seeders or leechers: {0} (S:{1} L:{2})".format(
                                        title, seeders, leechers))
                            continue

                        item = title, download_url, size, seeders, leechers
                        if mode != 'RSS':
                            sickrage.srCore.srLogger.debug("Found result: %s " % title)

                        items[mode].append(item)

                    except (AttributeError, TypeError, KeyError, ValueError):
                        continue

            # For each search mode sort all the items by seeders if available
            items[mode].sort(key=lambda tup: tup[3], reverse=True)

            results += items[mode]

        return results

    def seed_ratio(self):
        return self.ratio
