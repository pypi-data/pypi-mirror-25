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

import re

from .common import InfoExtractor
from ..compat import compat_str
from ..utils import (
    encode_base_n,
    ExtractorError,
    int_or_none,
    parse_duration,
    str_to_int,
)


class EpornerIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?eporner\.com/hd-porn/(?P<id>\w+)(?:/(?P<display_id>[\w-]+))?'
    _TESTS = [{
        'url': 'http://www.eporner.com/hd-porn/95008/Infamous-Tiffany-Teen-Strip-Tease-Video/',
        'md5': '39d486f046212d8e1b911c52ab4691f8',
        'info_dict': {
            'id': 'qlDUmNsj6VS',
            'display_id': 'Infamous-Tiffany-Teen-Strip-Tease-Video',
            'ext': 'mp4',
            'title': 'Infamous Tiffany Teen Strip Tease Video',
            'duration': 1838,
            'view_count': int,
            'age_limit': 18,
        },
    }, {
        # New (May 2016) URL layout
        'url': 'http://www.eporner.com/hd-porn/3YRUtzMcWn0/Star-Wars-XXX-Parody/',
        'only_matching': True,
    }, {
        'url': 'http://www.eporner.com/hd-porn/3YRUtzMcWn0',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')
        display_id = mobj.group('display_id') or video_id

        webpage, urlh = self._download_webpage_handle(url, display_id)

        video_id = self._match_id(compat_str(urlh.geturl()))

        hash = self._search_regex(
            r'hash\s*:\s*["\']([\da-f]{32})', webpage, 'hash')

        title = self._og_search_title(webpage, default=None) or self._html_search_regex(
            r'<title>(.+?) - EPORNER', webpage, 'title')

        # Reverse engineered from vjs.js
        def calc_hash(s):
            return ''.join((encode_base_n(int(s[lb:lb + 8], 16), 36) for lb in range(0, 32, 8)))

        video = self._download_json(
            'http://www.eporner.com/xhr/video/%s' % video_id,
            display_id, note='Downloading video JSON',
            query={
                'hash': calc_hash(hash),
                'device': 'generic',
                'domain': 'www.eporner.com',
                'fallback': 'false',
            })

        if video.get('available') is False:
            raise ExtractorError(
                '%s said: %s' % (self.IE_NAME, video['message']), expected=True)

        sources = video['sources']

        formats = []
        for kind, formats_dict in sources.items():
            if not isinstance(formats_dict, dict):
                continue
            for format_id, format_dict in formats_dict.items():
                if not isinstance(format_dict, dict):
                    continue
                src = format_dict.get('src')
                if not isinstance(src, compat_str) or not src.startswith('http'):
                    continue
                if kind == 'hls':
                    formats.extend(self._extract_m3u8_formats(
                        src, display_id, 'mp4', entry_protocol='m3u8_native',
                        m3u8_id=kind, fatal=False))
                else:
                    height = int_or_none(self._search_regex(
                        r'(\d+)[pP]', format_id, 'height', default=None))
                    fps = int_or_none(self._search_regex(
                        r'(\d+)fps', format_id, 'fps', default=None))

                    formats.append({
                        'url': src,
                        'format_id': format_id,
                        'height': height,
                        'fps': fps,
                    })
        self._sort_formats(formats)

        duration = parse_duration(self._html_search_meta('duration', webpage))
        view_count = str_to_int(self._search_regex(
            r'id="cinemaviews">\s*([0-9,]+)\s*<small>views',
            webpage, 'view count', fatal=False))

        return {
            'id': video_id,
            'display_id': display_id,
            'title': title,
            'duration': duration,
            'view_count': view_count,
            'formats': formats,
            'age_limit': 18,
        }
