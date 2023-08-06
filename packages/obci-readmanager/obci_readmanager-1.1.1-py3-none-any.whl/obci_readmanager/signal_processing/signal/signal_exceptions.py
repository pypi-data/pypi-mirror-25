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
#     Mateusz Kruszyński <mateusz.kruszynski@gmail.com>
#
"""Module provides classes for exceptions raised from DataProxy."""


class NoNextValue(Exception):
    """Raised when end of data file is met in self.get_next_value()."""


class NoNextTag(Exception):
    """Raised when end of tag file is met in self.get_next_tag()."""


class NoParameter(Exception):
    """Raised when there is a request for non-existing parameter in info file."""

    def __init__(self, p_param):
        """Initialize parameter."""
        self._param = p_param

    def __str__(self):
        """Return Exception message."""
        return "No parameter '{}' was found in info source!".format(self._param)


class BadSampleFormat(Exception):
    """
    An exception that should be raised when data sample has arrived and it is not float.

    Struct is unable to pack it.
    """

    def __str__(self):
        """Return Exception message."""
        return "Error! Received data sample is not of 'float' type! Writing to file aborted!"
