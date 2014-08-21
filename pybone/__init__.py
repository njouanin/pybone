# Copyright (C) 2014  Nicolas Jouanin
#
# This file is part of pybone.
#
# Pybone is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pybone is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pybone.  If not, see <http://www.gnu.org/licenses/>.

VERSION = (0, 0, 1, 'alpha', 0)

def _check_requirements():
    #Check python >= 3.4
    import sys
    if sys.version_info < (3, 4):
        raise ImportError("Python 3.4 or more is required")

_check_requirements()

#setup version
from pybone.utils.version import get_pretty_version
version_info = get_pretty_version(VERSION)
