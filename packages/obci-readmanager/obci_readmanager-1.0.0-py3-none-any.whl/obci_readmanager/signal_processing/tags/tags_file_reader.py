# OpenBCI - framework for Brain-Computer Interfaces based on EEG signal
# Project was initiated by Magdalena Michalska and Krzysztof Kulewski
# as part of their MSc theses at the University of Warsaw.
# Copyright (C) 2008-2009 Krzysztof Kulewski and Magdalena Michalska
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author:
#      Mateusz Kruszynski <mateusz.kruszynski@gmail.com>
#
"""Module provides a simple class that is able to read tags xml file and give on demand subsequential tags."""

import xml.dom.minidom
from functools import cmp_to_key

from . import tag_utils
from . import tags_logging as logger

LOGGER = logger.get_logger('tags_file_reader')


class TagsFileReader:
    """A simple class that is able to read tags xml file and give on demand subsequential tags."""

    def __init__(self, p_tags_file_name):
        """Init tags file path."""
        self._tags_file_name = p_tags_file_name
        self._tags = []
        self.start_tags_reading()

    def start_tags_reading(self):
        """Read tags file, store data in memory."""
        try:
            l_tags_file = open(self._tags_file_name, 'rt')
        except IOError:
            LOGGER.error("Couldn`t open tags file.")
        else:
            try:
                # Analyse xml info file, get what we want and close the file.
                self._parse_tags_file(l_tags_file)
            except xml.parsers.expat.ExpatError:
                LOGGER.error("An error occured while parsing tags xml file.")
            finally:
                l_tags_file.close()

    def get_tags(self):
        """Return next tag or None if all tags were alredy returned by this method."""
        return self._tags

    def _parse_tags_file(self, p_tags_file):
        """Parse p_tags_file xml tags file and store it in memory."""
        l_tags_doc = xml.dom.minidom.parse(p_tags_file)
        l_xml_root_element = l_tags_doc.getElementsByTagName("tags")[0]

        for i_tag_node in l_xml_root_element.getElementsByTagName("tag"):
            # Iterate over <tag> tags
            l_raw_tag = {}
            for i_key in ['length', 'name', 'position', 'channelNumber']:
                l_raw_tag[i_key] = i_tag_node.getAttribute(i_key)

            for i_node in i_tag_node.childNodes:
                try:
                    l_raw_tag[i_node.tagName] = i_node.firstChild.nodeValue
                except AttributeError:
                    pass
            # TODO - in case tags aren`t sorted by start_timestamp,
            # sort them at the end of current method
            self._tags.append(tag_utils.unpack_tag_from_dict(l_raw_tag))

        def cmp_tags(t1, t2):
            ts1 = t1['start_timestamp']
            ts2 = t2['start_timestamp']
            if ts1 == ts2:
                return 0
            elif ts1 > ts2:
                return 1
            else:
                return -1
        # warning - may slow down as hell
        self._tags.sort(key=cmp_to_key(cmp_tags))
