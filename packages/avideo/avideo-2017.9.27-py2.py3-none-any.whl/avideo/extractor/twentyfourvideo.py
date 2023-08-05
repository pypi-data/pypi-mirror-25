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
from ..utils import (
    parse_iso8601,
    int_or_none,
    xpath_attr,
    xpath_element,
)


class TwentyFourVideoIE(InfoExtractor):
    IE_NAME = '24video'
    _VALID_URL = r'https?://(?P<host>(?:www\.)?24video\.(?:net|me|xxx|sex|tube))/(?:video/(?:view|xml)/|player/new24_play\.swf\?id=)(?P<id>\d+)'

    _TESTS = [{
        'url': 'http://www.24video.net/video/view/1044982',
        'md5': 'e09fc0901d9eaeedac872f154931deeb',
        'info_dict': {
            'id': '1044982',
            'ext': 'mp4',
            'title': 'Эротика каменного века',
            'description': 'Как смотрели порно в каменном веке.',
            'thumbnail': r're:^https?://.*\.jpg$',
            'uploader': 'SUPERTELO',
            'duration': 31,
            'timestamp': 1275937857,
            'upload_date': '20100607',
            'age_limit': 18,
            'like_count': int,
            'dislike_count': int,
        },
    }, {
        'url': 'http://www.24video.net/player/new24_play.swf?id=1044982',
        'only_matching': True,
    }, {
        'url': 'http://www.24video.me/video/view/1044982',
        'only_matching': True,
    }, {
        'url': 'http://www.24video.tube/video/view/2363750',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')
        host = mobj.group('host')

        webpage = self._download_webpage(
            'http://%s/video/view/%s' % (host, video_id), video_id)

        title = self._og_search_title(webpage)
        description = self._html_search_regex(
            r'<(p|span)[^>]+itemprop="description"[^>]*>(?P<description>[^<]+)</\1>',
            webpage, 'description', fatal=False, group='description')
        thumbnail = self._og_search_thumbnail(webpage)
        duration = int_or_none(self._og_search_property(
            'duration', webpage, 'duration', fatal=False))
        timestamp = parse_iso8601(self._search_regex(
            r'<time id="video-timeago" datetime="([^"]+)" itemprop="uploadDate">',
            webpage, 'upload date'))

        uploader = self._html_search_regex(
            r'class="video-uploaded"[^>]*>\s*<a href="/jsecUser/movies/[^"]+"[^>]*>([^<]+)</a>',
            webpage, 'uploader', fatal=False)

        view_count = int_or_none(self._html_search_regex(
            r'<span class="video-views">(\d+) просмотр',
            webpage, 'view count', fatal=False))
        comment_count = int_or_none(self._html_search_regex(
            r'<a[^>]+href="#tab-comments"[^>]*>(\d+) комментари',
            webpage, 'comment count', fatal=False))

        # Sets some cookies
        self._download_xml(
            r'http://%s/video/xml/%s?mode=init' % (host, video_id),
            video_id, 'Downloading init XML')

        video_xml = self._download_xml(
            'http://%s/video/xml/%s?mode=play' % (host, video_id),
            video_id, 'Downloading video XML')

        video = xpath_element(video_xml, './/video', 'video', fatal=True)

        formats = [{
            'url': xpath_attr(video, '', 'url', 'video URL', fatal=True),
        }]

        like_count = int_or_none(video.get('ratingPlus'))
        dislike_count = int_or_none(video.get('ratingMinus'))
        age_limit = 18 if video.get('adult') == 'true' else 0

        return {
            'id': video_id,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'uploader': uploader,
            'duration': duration,
            'timestamp': timestamp,
            'view_count': view_count,
            'comment_count': comment_count,
            'like_count': like_count,
            'dislike_count': dislike_count,
            'age_limit': age_limit,
            'formats': formats,
        }
