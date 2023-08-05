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

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    js_to_json,
)


class OnDemandKoreaIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?ondemandkorea\.com/(?P<id>[^/]+)\.html'
    _GEO_COUNTRIES = ['US', 'CA']
    _TEST = {
        'url': 'http://www.ondemandkorea.com/ask-us-anything-e43.html',
        'info_dict': {
            'id': 'ask-us-anything-e43',
            'ext': 'mp4',
            'title': 'Ask Us Anything : E43',
            'thumbnail': r're:^https?://.*\.jpg$',
        },
        'params': {
            'skip_download': 'm3u8 download'
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id, fatal=False)

        if not webpage:
            # Page sometimes returns captcha page with HTTP 403
            raise ExtractorError(
                'Unable to access page. You may have been blocked.',
                expected=True)

        if 'msg_block_01.png' in webpage:
            self.raise_geo_restricted(
                msg='This content is not available in your region',
                countries=self._GEO_COUNTRIES)

        if 'This video is only available to ODK PLUS members.' in webpage:
            raise ExtractorError(
                'This video is only available to ODK PLUS members.',
                expected=True)

        title = self._og_search_title(webpage)

        jw_config = self._parse_json(
            self._search_regex(
                r'(?s)jwplayer\(([\'"])(?:(?!\1).)+\1\)\.setup\s*\((?P<options>.+?)\);',
                webpage, 'jw config', group='options'),
            video_id, transform_source=js_to_json)
        info = self._parse_jwplayer_data(
            jw_config, video_id, require_title=False, m3u8_id='hls',
            base_url=url)

        info.update({
            'title': title,
            'thumbnail': self._og_search_thumbnail(webpage),
        })
        return info
