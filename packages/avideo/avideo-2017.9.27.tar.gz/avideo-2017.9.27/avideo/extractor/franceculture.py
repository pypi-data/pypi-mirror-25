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
    determine_ext,
    extract_attributes,
    int_or_none,
)


class FranceCultureIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?franceculture\.fr/emissions/(?:[^/]+/)*(?P<id>[^/?#&]+)'
    _TEST = {
        'url': 'http://www.franceculture.fr/emissions/carnet-nomade/rendez-vous-au-pays-des-geeks',
        'info_dict': {
            'id': 'rendez-vous-au-pays-des-geeks',
            'display_id': 'rendez-vous-au-pays-des-geeks',
            'ext': 'mp3',
            'title': 'Rendez-vous au pays des geeks',
            'thumbnail': r're:^https?://.*\.jpg$',
            'upload_date': '20140301',
            'timestamp': 1393642916,
            'vcodec': 'none',
        }
    }

    def _real_extract(self, url):
        display_id = self._match_id(url)

        webpage = self._download_webpage(url, display_id)

        video_data = extract_attributes(self._search_regex(
            r'(?s)<div[^>]+class="[^"]*?(?:title-zone-diffusion|heading-zone-(?:wrapper|player-button))[^"]*?"[^>]*>.*?(<button[^>]+data-asset-source="[^"]+"[^>]+>)',
            webpage, 'video data'))

        video_url = video_data['data-asset-source']
        title = video_data.get('data-asset-title') or self._og_search_title(webpage)

        description = self._html_search_regex(
            r'(?s)<div[^>]+class="intro"[^>]*>.*?<h2>(.+?)</h2>',
            webpage, 'description', default=None)
        thumbnail = self._search_regex(
            r'(?s)<figure[^>]+itemtype="https://schema.org/ImageObject"[^>]*>.*?<img[^>]+(?:data-dejavu-)?src="([^"]+)"',
            webpage, 'thumbnail', fatal=False)
        uploader = self._html_search_regex(
            r'(?s)<span class="author">(.*?)</span>',
            webpage, 'uploader', default=None)
        ext = determine_ext(video_url.lower())

        return {
            'id': display_id,
            'display_id': display_id,
            'url': video_url,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'ext': ext,
            'vcodec': 'none' if ext == 'mp3' else None,
            'uploader': uploader,
            'timestamp': int_or_none(video_data.get('data-asset-created-date')),
            'duration': int_or_none(video_data.get('data-duration')),
        }
