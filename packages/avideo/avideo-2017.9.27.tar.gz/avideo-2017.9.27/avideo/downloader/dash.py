
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

from .fragment import FragmentFD
from ..compat import compat_urllib_error
from ..utils import urljoin


class DashSegmentsFD(FragmentFD):
    """
    Download segments in a DASH manifest
    """

    FD_NAME = 'dashsegments'

    def real_download(self, filename, info_dict):
        fragment_base_url = info_dict.get('fragment_base_url')
        fragments = info_dict['fragments'][:1] if self.params.get(
            'test', False) else info_dict['fragments']

        ctx = {
            'filename': filename,
            'total_frags': len(fragments),
        }

        self._prepare_and_start_frag_download(ctx)

        fragment_retries = self.params.get('fragment_retries', 0)
        skip_unavailable_fragments = self.params.get('skip_unavailable_fragments', True)

        frag_index = 0
        for i, fragment in enumerate(fragments):
            frag_index += 1
            if frag_index <= ctx['fragment_index']:
                continue
            # In DASH, the first segment contains necessary headers to
            # generate a valid MP4 file, so always abort for the first segment
            fatal = i == 0 or not skip_unavailable_fragments
            count = 0
            while count <= fragment_retries:
                try:
                    fragment_url = fragment.get('url')
                    if not fragment_url:
                        assert fragment_base_url
                        fragment_url = urljoin(fragment_base_url, fragment['path'])
                    success, frag_content = self._download_fragment(ctx, fragment_url, info_dict)
                    if not success:
                        return False
                    self._append_fragment(ctx, frag_content)
                    break
                except compat_urllib_error.HTTPError as err:
                    # YouTube may often return 404 HTTP error for a fragment causing the
                    # whole download to fail. However if the same fragment is immediately
                    # retried with the same request data this usually succeeds (1-2 attemps
                    # is usually enough) thus allowing to download the whole file successfully.
                    # To be future-proof we will retry all fragments that fail with any
                    # HTTP error.
                    count += 1
                    if count <= fragment_retries:
                        self.report_retry_fragment(err, frag_index, count, fragment_retries)
            if count > fragment_retries:
                if not fatal:
                    self.report_skip_fragment(frag_index)
                    continue
                self.report_error('giving up after %s fragment retries' % fragment_retries)
                return False

        self._finish_frag_download(ctx)

        return True
