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
import re

from .common import InfoExtractor
from ..aes import aes_cbc_decrypt
from ..compat import (
    compat_ord,
    compat_str,
)
from ..utils import (
    bytes_to_intlist,
    ExtractorError,
    intlist_to_bytes,
    int_or_none,
    strip_or_none,
)


class RTL2IE(InfoExtractor):
    IE_NAME = 'rtl2'
    _VALID_URL = r'http?://(?:www\.)?rtl2\.de/[^?#]*?/(?P<id>[^?#/]*?)(?:$|/(?:$|[?#]))'
    _TESTS = [{
        'url': 'http://www.rtl2.de/sendung/grip-das-motormagazin/folge/folge-203-0',
        'info_dict': {
            'id': 'folge-203-0',
            'ext': 'f4v',
            'title': 'GRIP sucht den Sommerkönig',
            'description': 'md5:e3adbb940fd3c6e76fa341b8748b562f'
        },
        'params': {
            # rtmp download
            'skip_download': True,
        },
    }, {
        'url': 'http://www.rtl2.de/sendung/koeln-50667/video/5512-anna/21040-anna-erwischt-alex/',
        'info_dict': {
            'id': '21040-anna-erwischt-alex',
            'ext': 'mp4',
            'title': 'Anna erwischt Alex!',
            'description': 'Anna nimmt ihrem Vater nicht ab, dass er nicht spielt. Und tatsächlich erwischt sie ihn auf frischer Tat.'
        },
        'params': {
            # rtmp download
            'skip_download': True,
        },
    }]

    def _real_extract(self, url):
        # Some rtl2 urls have no slash at the end, so append it.
        if not url.endswith('/'):
            url += '/'

        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        mobj = re.search(
            r'<div[^>]+data-collection="(?P<vico_id>\d+)"[^>]+data-video="(?P<vivi_id>\d+)"',
            webpage)
        if mobj:
            vico_id = mobj.group('vico_id')
            vivi_id = mobj.group('vivi_id')
        else:
            vico_id = self._html_search_regex(
                r'vico_id\s*:\s*([0-9]+)', webpage, 'vico_id')
            vivi_id = self._html_search_regex(
                r'vivi_id\s*:\s*([0-9]+)', webpage, 'vivi_id')

        info = self._download_json(
            'http://www.rtl2.de/sites/default/modules/rtl2/mediathek/php/get_video_jw.php',
            video_id, query={
                'vico_id': vico_id,
                'vivi_id': vivi_id,
            })
        video_info = info['video']
        title = video_info['titel']

        formats = []

        rtmp_url = video_info.get('streamurl')
        if rtmp_url:
            rtmp_url = rtmp_url.replace('\\', '')
            stream_url = 'mp4:' + self._html_search_regex(r'/ondemand/(.+)', rtmp_url, 'stream URL')
            rtmp_conn = ['S:connect', 'O:1', 'NS:pageUrl:' + url, 'NB:fpad:0', 'NN:videoFunction:1', 'O:0']

            formats.append({
                'format_id': 'rtmp',
                'url': rtmp_url,
                'play_path': stream_url,
                'player_url': 'http://www.rtl2.de/flashplayer/vipo_player.swf',
                'page_url': url,
                'flash_version': 'LNX 11,2,202,429',
                'rtmp_conn': rtmp_conn,
                'no_resume': True,
                'preference': 1,
            })

        m3u8_url = video_info.get('streamurl_hls')
        if m3u8_url:
            formats.extend(self._extract_akamai_formats(m3u8_url, video_id))

        self._sort_formats(formats)

        return {
            'id': video_id,
            'title': title,
            'thumbnail': video_info.get('image'),
            'description': video_info.get('beschreibung'),
            'duration': int_or_none(video_info.get('duration')),
            'formats': formats,
        }


class RTL2YouBaseIE(InfoExtractor):
    _BACKWERK_BASE_URL = 'https://p-you-backwerk.rtl2apps.de/'


class RTL2YouIE(RTL2YouBaseIE):
    IE_NAME = 'rtl2:you'
    _VALID_URL = r'http?://you\.rtl2\.de/(?:video/\d+/|youplayer/index\.html\?.*?\bvid=)(?P<id>\d+)'
    _TESTS = [{
        'url': 'http://you.rtl2.de/video/3002/15740/MJUNIK%20%E2%80%93%20Home%20of%20YOU/307-hirn-wo-bist-du',
        'info_dict': {
            'id': '15740',
            'ext': 'mp4',
            'title': 'MJUNIK – Home of YOU - #307 Hirn, wo bist du?!',
            'description': 'md5:ddaa95c61b372b12b66e115b2772fe01',
            'age_limit': 12,
        },
    }, {
        'url': 'http://you.rtl2.de/youplayer/index.html?vid=15712',
        'only_matching': True,
    }]
    _AES_KEY = b'\xe9W\xe4.<*\xb8\x1a\xd2\xb6\x92\xf3C\xd3\xefL\x1b\x03*\xbbbH\xc0\x03\xffo\xc2\xf2(\xaa\xaa!'
    _GEO_COUNTRIES = ['DE']

    def _real_extract(self, url):
        video_id = self._match_id(url)

        stream_data = self._download_json(
            self._BACKWERK_BASE_URL + 'stream/video/' + video_id, video_id)

        data, iv = base64.b64decode(stream_data['streamUrl']).decode().split(':')
        stream_url = intlist_to_bytes(aes_cbc_decrypt(
            bytes_to_intlist(base64.b64decode(data)),
            bytes_to_intlist(self._AES_KEY),
            bytes_to_intlist(base64.b64decode(iv))
        ))
        if b'rtl2_you_video_not_found' in stream_url:
            raise ExtractorError('video not found', expected=True)

        formats = self._extract_m3u8_formats(
            stream_url[:-compat_ord(stream_url[-1])].decode(),
            video_id, 'mp4', 'm3u8_native')
        self._sort_formats(formats)

        video_data = self._download_json(
            self._BACKWERK_BASE_URL + 'video/' + video_id, video_id)

        series = video_data.get('formatTitle')
        title = episode = video_data.get('title') or series
        if series and series != title:
            title = '%s - %s' % (series, title)

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'description': strip_or_none(video_data.get('description')),
            'thumbnail': video_data.get('image'),
            'duration': int_or_none(stream_data.get('duration') or video_data.get('duration'), 1000),
            'series': series,
            'episode': episode,
            'age_limit': int_or_none(video_data.get('minimumAge')),
        }


class RTL2YouSeriesIE(RTL2YouBaseIE):
    IE_NAME = 'rtl2:you:series'
    _VALID_URL = r'http?://you\.rtl2\.de/videos/(?P<id>\d+)'
    _TEST = {
        'url': 'http://you.rtl2.de/videos/115/dragon-ball',
        'info_dict': {
            'id': '115',
        },
        'playlist_mincount': 5,
    }

    def _real_extract(self, url):
        series_id = self._match_id(url)
        stream_data = self._download_json(
            self._BACKWERK_BASE_URL + 'videos',
            series_id, query={
                'formatId': series_id,
                'limit': 1000000000,
            })

        entries = []
        for video in stream_data.get('videos', []):
            video_id = compat_str(video['videoId'])
            if not video_id:
                continue
            entries.append(self.url_result(
                'http://you.rtl2.de/video/%s/%s' % (series_id, video_id),
                'RTL2You', video_id))
        return self.playlist_result(entries, series_id)
