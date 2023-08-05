
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
from ..utils import ExtractorError


class TestURLIE(InfoExtractor):
    """ Allows addressing of the test cases as test:yout.*be_1 """

    IE_DESC = False  # Do not list
    _VALID_URL = r'test(?:url)?:(?P<id>(?P<extractor>.+?)(?:_(?P<num>[0-9]+))?)$'

    def _real_extract(self, url):
        from ..extractor import gen_extractors

        mobj = re.match(self._VALID_URL, url)
        video_id = mobj.group('id')
        extractor_id = mobj.group('extractor')
        all_extractors = gen_extractors()

        rex = re.compile(extractor_id, flags=re.IGNORECASE)
        matching_extractors = [
            e for e in all_extractors if rex.search(e.IE_NAME)]

        if len(matching_extractors) == 0:
            raise ExtractorError(
                'No extractors matching %r found' % extractor_id,
                expected=True)
        elif len(matching_extractors) > 1:
            # Is it obvious which one to pick?
            try:
                extractor = next(
                    ie for ie in matching_extractors
                    if ie.IE_NAME.lower() == extractor_id.lower())
            except StopIteration:
                raise ExtractorError(
                    ('Found multiple matching extractors: %s' %
                        ' '.join(ie.IE_NAME for ie in matching_extractors)),
                    expected=True)
        else:
            extractor = matching_extractors[0]

        num_str = mobj.group('num')
        num = int(num_str) if num_str else 0

        testcases = []
        t = getattr(extractor, '_TEST', None)
        if t:
            testcases.append(t)
        testcases.extend(getattr(extractor, '_TESTS', []))

        try:
            tc = testcases[num]
        except IndexError:
            raise ExtractorError(
                ('Test case %d not found, got only %d tests' %
                    (num, len(testcases))),
                expected=True)

        self.to_screen('Test URL: %s' % tc['url'])

        return {
            '_type': 'url',
            'url': tc['url'],
            'id': video_id,
        }
