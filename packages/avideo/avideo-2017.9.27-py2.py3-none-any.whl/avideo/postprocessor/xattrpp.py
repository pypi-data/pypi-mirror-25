
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

from .common import PostProcessor
from ..compat import compat_os_name
from ..utils import (
    hyphenate_date,
    write_xattr,
    XAttrMetadataError,
    XAttrUnavailableError,
)


class XAttrMetadataPP(PostProcessor):

    #
    # More info about extended attributes for media:
    #   http://freedesktop.org/wiki/CommonExtendedAttributes/
    #   http://www.freedesktop.org/wiki/PhreedomDraft/
    #   http://dublincore.org/documents/usageguide/elements.shtml
    #
    # TODO:
    #  * capture youtube keywords and put them in 'user.dublincore.subject' (comma-separated)
    #  * figure out which xattrs can be used for 'duration', 'thumbnail', 'resolution'
    #

    def run(self, info):
        """ Set extended attributes on downloaded file (if xattr support is found). """

        # Write the metadata to the file's xattrs
        self._downloader.to_screen('[metadata] Writing metadata to file\'s xattrs')

        filename = info['filepath']

        try:
            xattr_mapping = {
                'user.xdg.referrer.url': 'webpage_url',
                # 'user.xdg.comment':            'description',
                'user.dublincore.title': 'title',
                'user.dublincore.date': 'upload_date',
                'user.dublincore.description': 'description',
                'user.dublincore.contributor': 'uploader',
                'user.dublincore.format': 'format',
            }

            for xattrname, infoname in xattr_mapping.items():

                value = info.get(infoname)

                if value:
                    if infoname == 'upload_date':
                        value = hyphenate_date(value)

                    byte_value = value.encode('utf-8')
                    write_xattr(filename, xattrname, byte_value)

            return [], info

        except XAttrUnavailableError as e:
            self._downloader.report_error(str(e))
            return [], info

        except XAttrMetadataError as e:
            if e.reason == 'NO_SPACE':
                self._downloader.report_warning(
                    'There\'s no disk space left or disk quota exceeded. ' +
                    'Extended attributes are not written.')
            elif e.reason == 'VALUE_TOO_LONG':
                self._downloader.report_warning(
                    'Unable to write extended attributes due to too long values.')
            else:
                msg = 'This filesystem doesn\'t support extended attributes. '
                if compat_os_name == 'nt':
                    msg += 'You need to use NTFS.'
                else:
                    msg += '(You may have to enable them in your /etc/fstab)'
                self._downloader.report_error(msg)
            return [], info
