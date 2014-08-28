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
import multiprocessing
import platform

_loop = asyncio.get_event_loop()

LOGGER = logging.getLogger(__name__)


class PlatformError(Exception):
    pass


class Platform:
    """
    Base class for platform configuration
    """
    def __repr__(self):
        return "%s(system_name=%r,kernel_release=%r,processor=%r)" % (self.__class__.__name__,
                                                                      self.os_name,
                                                                      self.kernel_release,
                                                                      self.processor)

    def __init__(self):
        self.os_name = platform.system()
        self.kernel_release = platform.release()
        self.processor = platform.processor() or platform.machine()
        try:
            self.processor_count = multiprocessing.cpu_count()
        except NotImplemented:
            self.processor_count = 1

    def read_board_info(self):
        pass

    @asyncio.coroutine
    def read_pins_file(self):
        pass

    @asyncio.coroutine
    def read_pinmux_pins(self):
        pass

from .linux_3_8 import Linux38Platform

#try:
#    from pybone.bone_3_8.config import Linux38Config
#    local_config = Linux38Config(local_system, local_release, local_processor)
#except PlatformError:
#    LOGGER.warn("Not running on a BBB")
#    local_config = Platform(local_system, local_release, local_processor)
