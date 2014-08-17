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

import platform
import asyncio
from pybone.utils.filesystem import find_first_file

_loop = asyncio.get_event_loop()


class PlatformError(Exception):
    pass


class Config(object):
    """
    Base class for board configuration
    """
    def __init__(self, system_name, kernel_release, processor):
        self.system_name = system_name
        self.kernel_release = kernel_release
        self.processor = processor

    def __repr__(self):
        return "%s(system_name=%r,kernel_release=%r,processor=%r)" % \
               (self.__class__.__name__,
                self.system_name,
                self.kernel_release,
                self.processor)


local_system = platform.system()
local_release = platform.release()
local_processor = platform.processor()
try:
    from pybone.bone_3_8.config import Linux38Config
    local_config = Linux38Config(local_system, local_release, local_processor)
except PlatformError:
    local_config = Config(local_system, local_release, local_processor)
