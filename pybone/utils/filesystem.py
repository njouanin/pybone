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

import asyncio
import logging
import glob

LOGGER = logging.getLogger(__name__)

@asyncio.coroutine
def read_async(file):
    """
    File reading coroutine
    """
    try:
        fp = open(file)
    except PermissionError:
        LOGGER.warning("Permission error while reading %s. Consider running as root or some sudoers." % file)
        return None
    else:
        return fp.readlines()


@asyncio.coroutine
def find_first_file(pattern):
    """
    Find first file matching a file pattern
    """
    return glob.iglob(pattern)[0]
