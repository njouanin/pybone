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
from pybone.bone import Platform, PlatformError
from pybone.utils import filesystem

LOGGER = logging.getLogger(__name__)


def get_board_name(board_id):
    boards = {
        'A335BONE': 'BeagleBone',
        'A335BNLT': 'BeagleBone Black'
    }
    try:
        board_name = boards[board_id]
    except KeyError:
        board_name = None
    return board_name


@asyncio.coroutine
def read_board_name(board_file):
    LOGGER.debug("BEGIN read_board_name")
    file_content = yield from filesystem.read_async(board_file)
    board_id = file_content[0].strip()
    board_name = get_board_name(board_id)
    if board_name is None:
        LOGGER.warning("Unexpected board id '%s", board_id)
    LOGGER.debug("END read_board_name")
    return board_name


@asyncio.coroutine
def read_board_revision(revision_file):
    LOGGER.debug("BEGIN read_board_revision")
    file_content = yield from filesystem.read_async(revision_file)
    if file_content is None:
        return None
    else:
        LOGGER.debug("END read_board_revision")
        return file_content[0].strip()


@asyncio.coroutine
def read_board_serial_number(serial_number_file):
    LOGGER.debug("BEGIN read_board_serial_number")
    file_content = yield from filesystem.read_async(serial_number_file)
    if file_content is None:
        return None
    else:
        LOGGER.debug("END read_board_serial_number")
        return file_content[0].strip()


class Linux38Platform(Platform):
    """
    Linux running on BeagleBone platform
    This should match the system configuration running on a beagleboard
    """
    _BOARD_NAME_FILE = '/sys/devices/bone_capemgr.*/baseboard/board-name'
    _REVISION_FILE = '/sys/devices/bone_capemgr.*/baseboard/revision'
    _SERIAL_NUMBER_FILE = '/sys/devices/bone_capemgr.*/baseboard/serial-number'
    _PINS_FILE = '/sys/kernel/debug/pinctrl/44e10800.pinmux/pins'
    _PINMUX_FILE = '/sys/kernel/debug/pinctrl/44e10800.pinmux/pinmux-pins'


    def __init__(self, loop=None):
        super().__init__()
        if 'Linux' not in self.os_name:
            raise PlatformError("Unexpected system name '%r'" % self.os_name)
        elif '3.8' not in self.kernel_release:
            raise PlatformError("Unexpected kernel release '%r'" % self.kernel_release)
        elif 'arm' not in self.processor:
            raise PlatformError("Unexpected processor '%r'" % self.processor)

        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop
        (self.board_name_file,
         self.revision_file,
         self.serial_number_file,
         self.pins_file,
         self.pinmux_pins_file) = self._loop.run_until_complete(asyncio.gather(
            filesystem.find_first_file(Linux38Platform._BOARD_NAME_FILE),
            filesystem.find_first_file(Linux38Platform._REVISION_FILE),
            filesystem.find_first_file(Linux38Platform._SERIAL_NUMBER_FILE),
            filesystem.find_first_file(Linux38Platform._PINS_FILE),
            filesystem.find_first_file(Linux38Platform._PINMUX_FILE)))

    def read_board_info(self, loop=None):
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop
        board_name = asyncio.async(read_board_name(self.board_name_file))
        board_revision = asyncio.async(read_board_revision(self.revision_file))
        board_serial_number = asyncio.async(read_board_serial_number(self.serial_number_file))

        self._loop.run_until_complete(asyncio.wait([board_name, board_revision, board_serial_number]))
        return board_name, board_revision, board_serial_number

    def iterate_pins_file(self, loop=None):
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop
        file_content = asyncio.async(filesystem.read_async(self.pins_file))
        self._loop.run_until_complete(file_content)
        if file_content is not None:
            return map(parse_pins_line, file_content[1:])
        else:
            return None
