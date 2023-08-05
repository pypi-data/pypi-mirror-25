
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
from ..utils import (
    NO_DEFAULT,
    str_to_int,
)


class DrTuberIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?drtuber\.com/(?:video|embed)/(?P<id>\d+)(?:/(?P<display_id>[\w-]+))?'
    _TESTS = [{
        'url': 'http://www.drtuber.com/video/1740434/hot-perky-blonde-naked-golf',
        'md5': '93e680cf2536ad0dfb7e74d94a89facd',
        'info_dict': {
            'id': '1740434',
            'display_id': 'hot-perky-blonde-naked-golf',
            'ext': 'mp4',
            'title': 'hot perky blonde naked golf',
            'like_count': int,
            'comment_count': int,
            'categories': ['Babe', 'Blonde', 'Erotic', 'Outdoor', 'Softcore', 'Solo'],
            'thumbnail': r're:https?://.*\.jpg$',
            'age_limit': 18,
        }
    }, {
        'url': 'http://www.drtuber.com/embed/489939',
        'only_matching': True,
    }]

    @staticmethod
    def _extract_urls(webpage):
        return re.findall(
            r'<iframe[^>]+?src=["\'](?P<url>(?:https?:)?//(?:www\.)?drtuber\.com/embed/\d+)',
            webpage)

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')
        display_id = mobj.group('display_id') or video_id

        webpage = self._download_webpage(
            'http://www.drtuber.com/video/%s' % video_id, display_id)

        video_data = self._download_json(
            'http://www.drtuber.com/player_config_json/', video_id, query={
                'vid': video_id,
                'embed': 0,
                'aid': 0,
                'domain_id': 0,
            })

        formats = []
        for format_id, video_url in video_data['files'].items():
            if video_url:
                formats.append({
                    'format_id': format_id,
                    'quality': 2 if format_id == 'hq' else 1,
                    'url': video_url
                })
        self._sort_formats(formats)

        title = self._html_search_regex(
            (r'class="title_watch"[^>]*><(?:p|h\d+)[^>]*>([^<]+)<',
             r'<p[^>]+class="title_substrate">([^<]+)</p>',
             r'<title>([^<]+) - \d+'),
            webpage, 'title')

        thumbnail = self._html_search_regex(
            r'poster="([^"]+)"',
            webpage, 'thumbnail', fatal=False)

        def extract_count(id_, name, default=NO_DEFAULT):
            return str_to_int(self._html_search_regex(
                r'<span[^>]+(?:class|id)="%s"[^>]*>([\d,\.]+)</span>' % id_,
                webpage, '%s count' % name, default=default, fatal=False))

        like_count = extract_count('rate_likes', 'like')
        dislike_count = extract_count('rate_dislikes', 'dislike', default=None)
        comment_count = extract_count('comments_count', 'comment')

        cats_str = self._search_regex(
            r'<div[^>]+class="categories_list">(.+?)</div>',
            webpage, 'categories', fatal=False)
        categories = [] if not cats_str else re.findall(
            r'<a title="([^"]+)"', cats_str)

        return {
            'id': video_id,
            'display_id': display_id,
            'formats': formats,
            'title': title,
            'thumbnail': thumbnail,
            'like_count': like_count,
            'dislike_count': dislike_count,
            'comment_count': comment_count,
            'categories': categories,
            'age_limit': self._rta_search(webpage),
        }
