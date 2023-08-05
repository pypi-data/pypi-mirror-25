# coding: utf-8

# Copyright (C) 2017 avideo authors (see AUTHORS)

#
#    This file is part of avideo.
#
#    avideo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    avideo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with avideo.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import base64
import json

from .common import InfoExtractor
from ..compat import (
    compat_urlparse,
    compat_str,
)
from ..utils import (
    extract_attributes,
    ExtractorError,
    get_elements_by_class,
    urlencode_postdata,
)


class EinthusanIE(InfoExtractor):
    _VALID_URL = r'https?://einthusan\.tv/movie/watch/(?P<id>[^/?#&]+)'
    _TESTS = [{
        'url': 'https://einthusan.tv/movie/watch/9097/',
        'md5': 'ff0f7f2065031b8a2cf13a933731c035',
        'info_dict': {
            'id': '9097',
            'ext': 'mp4',
            'title': 'Ae Dil Hai Mushkil',
            'description': 'md5:33ef934c82a671a94652a9b4e54d931b',
            'thumbnail': r're:^https?://.*\.jpg$',
        }
    }, {
        'url': 'https://einthusan.tv/movie/watch/51MZ/?lang=hindi',
        'only_matching': True,
    }]

    # reversed from jsoncrypto.prototype.decrypt() in einthusan-PGMovieWatcher.js
    def _decrypt(self, encrypted_data, video_id):
        return self._parse_json(base64.b64decode((
            encrypted_data[:10] + encrypted_data[-1] + encrypted_data[12:-1]
        ).encode('ascii')).decode('utf-8'), video_id)

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        title = self._html_search_regex(r'<h3>([^<]+)</h3>', webpage, 'title')

        player_params = extract_attributes(self._search_regex(
            r'(<section[^>]+id="UIVideoPlayer"[^>]+>)', webpage, 'player parameters'))

        page_id = self._html_search_regex(
            '<html[^>]+data-pageid="([^"]+)"', webpage, 'page ID')
        video_data = self._download_json(
            'https://einthusan.tv/ajax/movie/watch/%s/' % video_id, video_id,
            data=urlencode_postdata({
                'xEvent': 'UIVideoPlayer.PingOutcome',
                'xJson': json.dumps({
                    'EJOutcomes': player_params['data-ejpingables'],
                    'NativeHLS': False
                }),
                'arcVersion': 3,
                'appVersion': 59,
                'gorilla.csrf.Token': page_id,
            }))['Data']

        if isinstance(video_data, compat_str) and video_data.startswith('/ratelimited/'):
            raise ExtractorError(
                'Download rate reached. Please try again later.', expected=True)

        ej_links = self._decrypt(video_data['EJLinks'], video_id)

        formats = []

        m3u8_url = ej_links.get('HLSLink')
        if m3u8_url:
            formats.extend(self._extract_m3u8_formats(
                m3u8_url, video_id, ext='mp4', entry_protocol='m3u8_native'))

        mp4_url = ej_links.get('MP4Link')
        if mp4_url:
            formats.append({
                'url': mp4_url,
            })

        self._sort_formats(formats)

        description = get_elements_by_class('synopsis', webpage)[0]
        thumbnail = self._html_search_regex(
            r'''<img[^>]+src=(["'])(?P<url>(?!\1).+?/moviecovers/(?!\1).+?)\1''',
            webpage, 'thumbnail url', fatal=False, group='url')
        if thumbnail is not None:
            thumbnail = compat_urlparse.urljoin(url, thumbnail)

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'thumbnail': thumbnail,
            'description': description,
        }
