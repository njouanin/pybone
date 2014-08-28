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
import re
from pybone.bone import Platform, PlatformError
from pybone.bone.pin import RegPullEnum, RegPullTypeEnum, RegRcvEnum, RegSlewEnum
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

    @asyncio.coroutine
    def read_pins_file(self):
        def parse_pins_line(line):
            m = re.match(r"pin ([0-9]+)\s.([0-9a-f]+).\s([0-9a-f]+)", line)
            try:
                pin_index = int(m.group(1))
                pin_address = int(m.group(2), 16)
                reg = int(m.group(3), 16)
                #Extract register configuration
                # bit 0-2: pin mode
                # bit 3 : pullup/down enable/disable (0=enable, 1=disable)
                # bit 4 : pullup/down selection (0=pulldown, 1=pullup)
                # bit 5 : input enable (0=input disable, 1=input enable)
                # bit 6 : slew rate (0=fast, 1=slow)
                pin_reg = {'mode': reg & 0x07,
                           'slew': RegSlewEnum.slow if (reg & 0x40) else RegSlewEnum.fast,
                           'receive': RegRcvEnum.enabled if (reg & 0x20) else RegRcvEnum.disabled,
                           'pull': RegPullEnum.enabled if ((reg >> 3) & 0x01) else RegPullEnum.disabled,
                           'pulltype': RegPullTypeEnum.pullup if ((reg >> 4) & 0x01) else RegPullTypeEnum.pulldown}

                return {'index': pin_index, 'address': pin_address, 'reg': pin_reg}
            except Exception as e:
                LOGGER.warning("Failed parsing pins line '%s'." % line, e)
                return None

        file_content = yield from filesystem.read_async(self.pins_file)
        if file_content is not None:
            return map(parse_pins_line, file_content[1:])
        else:
            return None

    @asyncio.coroutine
    def read_pinmux_pins(self):
        def parse_pinmux_pins_file(line):
            #pin 0 (44e10800): mmc.10 (GPIO UNCLAIMED) function pinmux_emmc2_pins group pinmux_emmc2_pins
            #pin 8 (44e10820): (MUX UNCLAIMED) (GPIO UNCLAIMED)

            m = re.match(r"pin ([0-9]+)\s.([0-9a-f]+).\:.(.*)", line)
            if m is None:
                LOGGER.warning("pinmux line '%s' doesn't find expected format." % line)
                return None
            pin_index = int(m.group(1))
            pin_address = int(m.group(2), 16)
            owner_string = m.group(3)

            if '(MUX UNCLAIMED) (GPIO UNCLAIMED)' in owner_string:
                pin_mux_owner = None
                pin_gpio_owner = None
                pin_function = None
                pin_group = None
            elif '(MUX UNCLAIMED)' in owner_string:
                m = re.match(r"\(MUX UNCLAIMED\) ([\(\)\w\.\d_]+) function ([\(\)\w\.\d_]+) group ([\(\)\w\.\d_]+)",
                             owner_string)
                if m is None:
                    LOGGER.warning("pinmux line '%s' doesn't find expected format." % line)
                    return None
                else:
                    pin_mux_owner = None
                    pin_gpio_owner = m.group(1)
                    pin_function = m.group(2)
                    pin_group = m.group(3)
            elif '(GPIO UNCLAIMED)' in owner_string:
                m = re.match(r"([\(\)\w\.\d_]+) \(GPIO UNCLAIMED\) function ([\(\)\w\.\d_]+) group ([\(\)\w\.\d_]+)",
                             owner_string)
                if m is None:
                    LOGGER.warning("pinmux line '%s' doesn't find expected format." % line)
                    return None
                else:
                    pin_mux_owner = m.group(1)
                    pin_gpio_owner = None
                    pin_function = m.group(2)
                    pin_group = m.group(3)
            else:
                LOGGER.warning("pinmux line '%s' doesn't find expected format." % line)
                return None

            return {'index': pin_index,
               'address': pin_address,
               'mux_owner': pin_mux_owner,
               'gpio_owner': pin_gpio_owner,
               'function': pin_function,
               'group': pin_group
            }

        file_content = yield from filesystem.read_async(self.pinmux_pins_file)
        if file_content is not None:
            return map(parse_pinmux_pins_file, file_content[2:])
        else:
            return None
