
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

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    HEADRequest,
    sanitized_Request,
    urlencode_postdata,
)


class HotNewHipHopIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?hotnewhiphop\.com/.*\.(?P<id>.*)\.html'
    _TEST = {
        'url': 'http://www.hotnewhiphop.com/freddie-gibbs-lay-it-down-song.1435540.html',
        'md5': '2c2cd2f76ef11a9b3b581e8b232f3d96',
        'info_dict': {
            'id': '1435540',
            'ext': 'mp3',
            'title': 'Freddie Gibbs - Lay It Down'
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        video_url_base64 = self._search_regex(
            r'data-path="(.*?)"', webpage, 'video URL', default=None)

        if video_url_base64 is None:
            video_url = self._search_regex(
                r'"contentUrl" content="(.*?)"', webpage, 'content URL')
            return self.url_result(video_url, ie='Youtube')

        reqdata = urlencode_postdata([
            ('mediaType', 's'),
            ('mediaId', video_id),
        ])
        r = sanitized_Request(
            'http://www.hotnewhiphop.com/ajax/media/getActions/', data=reqdata)
        r.add_header('Content-Type', 'application/x-www-form-urlencoded')
        mkd = self._download_json(
            r, video_id, note='Requesting media key',
            errnote='Could not download media key')
        if 'mediaKey' not in mkd:
            raise ExtractorError('Did not get a media key')

        redirect_url = base64.b64decode(video_url_base64).decode('utf-8')
        redirect_req = HEADRequest(redirect_url)
        req = self._request_webpage(
            redirect_req, video_id,
            note='Resolving final URL', errnote='Could not resolve final URL')
        video_url = req.geturl()
        if video_url.endswith('.html'):
            raise ExtractorError('Redirect failed')

        video_title = self._og_search_title(webpage).strip()

        return {
            'id': video_id,
            'url': video_url,
            'title': video_title,
            'thumbnail': self._og_search_thumbnail(webpage),
        }
