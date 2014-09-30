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
from .pinctrl import parse_pinmux_pins_file, parse_pins_line

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
    file_content = yield from filesystem.read_async(board_file)
    try:
        board_id = file_content[0].strip()
    except:
        msg = "Unexpected content in board_file %s" % board_file
        LOGGER.warning(msg)
        raise PlatformError(msg)
    board_name = get_board_name(board_id)
    if board_name is None:
        msg = "Unexpected board id '%s" % board_id
        LOGGER.warning(msg)
        raise PlatformError(msg)
    return board_name


@asyncio.coroutine
def read_board_revision(revision_file):
    file_content = yield from filesystem.read_async(revision_file)
    try:
        board_revision = file_content[0].strip()
        return board_revision
    except:
        msg = "Unexpected content in revision_file %s" % revision_file
        LOGGER.warning(msg)
        raise PlatformError(msg)


@asyncio.coroutine
def read_board_serial_number(serial_number_file):
    LOGGER.debug("BEGIN read_board_serial_number")
    file_content = yield from filesystem.read_async(serial_number_file)
    try:
        serial_number = file_content[0].strip()
        return  serial_number
    except:
        msg = "Unexpected content in serial_number_file %s" % serial_number_file
        LOGGER.warning(msg)
        raise PlatformError(msg)


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
            raise PlatformError("Expected Linux OS, found '%r'" % self.os_name)
        elif '3.8' not in self.kernel_release:
            raise PlatformError("Expected kernel 3.8, found release '%r'" % self.kernel_release)
        elif 'arm' not in self.processor:
            raise PlatformError("Expected ARM processor, found '%r'" % self.processor)

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
        t1 = asyncio.async(read_board_name(self.board_name_file))
        t2 = asyncio.async(read_board_revision(self.revision_file))
        t3 = asyncio.async(read_board_serial_number(self.serial_number_file))

        #returns (board_name, board_revision, board_serial_number) results
        try:
            (board_name, board_revision, board_serial_number) = \
                self._loop.run_until_complete(asyncio.gather(t1, t2, t3))
        except PlatformError as pe:
            raise pe
        except:
            raise PlatformError("Error while reading board informations")
        return board_name, board_revision, board_serial_number

    @asyncio.coroutine
    def read_pins_file(self):
        file_content = yield from filesystem.read_async(self.pins_file, self._loop)
        if file_content is not None:
            return map(parse_pins_line, file_content[1:])
        else:
            raise PlatformError("Couldn't read pins file " % self.pins_file)

    @asyncio.coroutine
    def read_pinmux_pins(self):
        file_content = yield from filesystem.read_async(self.pinmux_pins_file, self._loop)
        if file_content is not None:
            return map(parse_pinmux_pins_file, file_content[2:])
        else:
            raise PlatformError("Couldn't read pinmux file " % self.pinmux_pins_file)
