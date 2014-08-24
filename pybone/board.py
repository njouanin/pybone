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
from enum import Enum
from pybone.pin_desc import BBB_P8_DEF, BBB_P9_DEF
from pybone.utils import filesystem
from pybone.config import local_config

LOGGER = logging.getLogger(__name__)
loop = asyncio.get_event_loop()


class PlatformError(Exception):
    pass


class Header(Enum):
    p8 = 'P8'
    p9 = 'P9'
    board = 'board'


class RegSlew(Enum):
    slow = 'slow'
    fast = 'fast'


class RegRcv(Enum):
    enabled = 'enabled'
    disabled = 'disabled'


class RegPull(Enum):
    enabled = 'enabled'
    disabled = 'disabled'


class RegPullType(Enum):
    pullup = 'pullup'
    pulldown = 'pulldown'


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
                   'slew': RegSlew.slow if (reg & 0x40) else RegSlew.fast,
                   'receive': RegRcv.enabled if (reg & 0x20) else RegRcv.disabled,
                   'pull': RegPull.enabled if ((reg >> 3) & 0x01) else RegPull.disabled,
                   'pulltype': RegPullType.pullup if ((reg >> 4) & 0x01) else RegPullType.pulldown}

        return {'index': pin_index, 'address': pin_address, 'reg': pin_reg}
    except Exception as e:
        LOGGER.warning("Failed parsing pins line '%s'." % line, e)
        return None


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


@asyncio.coroutine
def read_pins_file(pins_file):
    file_content = yield from filesystem.read_async(pins_file)
    if file_content is not None:
        return map(parse_pins_line, file_content[1:])
    else:
        return None


@asyncio.coroutine
def read_pinmux_pins(pinmux_pins_file):
    file_content = yield from filesystem.read_async(pinmux_pins_file)
    if file_content is not None:
        return map(parse_pinmux_pins_file, file_content[2:])
    else:
        return None


@asyncio.coroutine
def read_board_name(board_file):
    LOGGER.debug("BEGIN read_board_name")
    file_content = yield from filesystem.read_async(board_file)
    if file_content is None:
        boardname = None
    else:
        boardname = file_content[0].strip()
        if boardname == 'A335BONE':
            boardname = 'BeagleBone'
        elif boardname == 'A335BNLT':
            boardname = 'BeagleBone Black'
        else:
            LOGGER.warning("Unexpected board name '%s", boardname)
    LOGGER.debug("END read_board_name")
    return boardname


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


class Pin(object):
    def __init__(self, board, definition):
        self.board = board
        self.header = definition['header']
        self.header_pin = definition['head_pin']
        self.header_name = definition['head_name']
        self.proc_pin = definition['proc_pin']
        self.proc_pin_name = definition['proc_pin_name']
        self.proc_signal_name = definition['proc_signal_name']
        self.reg_offset = definition['reg_offset']
        self.driver_pin = definition['driver_pin']
        self.reset_mode = definition['reset_mode']
        self.gpio_chip = definition['gpio_chip']
        self.gpio_number = definition['gpio_number']

    def update_from_pins(self, pins_info):
        if self.address == pins_info['address']:
            self.register_mode = pins_info['reg']['mode']
            self.register_slew = pins_info['reg']['slew']
            self.register_receive = pins_info['reg']['receive']
            self.register_pull = pins_info['reg']['pull']
            self.register_pulltype = pins_info['reg']['pulltype']
        else:
            LOGGER.debug("Pin address configuration '0x%x' doesn't match pins address '0x%x" % (self.address, pins_info['address']))

    def update_from_pinmux_pins(self, pinmux_info):
        if self.address == pinmux_info['address']:
            self.mux_owner = pinmux_info['mux_owner']
            self.gpio_owner = pinmux_info['gpio_owner']
            self.function = pinmux_info['function']
            self.group = pinmux_info['group']
        else:
            LOGGER.debug("Pin address configuration '0x%x' doesn't match pinmux address '0x%x" % (self.address, pinmux_info['address']))

    @property
    def address(self):
        if self.reg_offset is not None:
            return Board.pin_reg_address + self.reg_offset
        else:
            return 0

    @property
    def key(self):
        return "%s_%d" % (self.header.value, self.header_pin)

    def __repr__(self):
        sb = []
        for key in self.__dict__:
            sb.append("%r=%r" % (key, self.__dict__[key]))
        return "Pin(" + ','.join(sb) + ")"


class Board(object):
    pin_reg_address = 0x44e10000

    def __init__(self, run_platform=local_config):
        self.platform = run_platform
        loop.run_until_complete(self._init_async())
        self.pins = [pin for pin in self._load_pins(Header.p8)]
        self.pins += [pin for pin in self._load_pins(Header.p9)]
        loop.run_until_complete(self._update_from_pinctrl())

    @asyncio.coroutine
    def _init_async(self):
        try:
            (self.name, self.revision, self.serial_number) = yield from asyncio.gather(
                read_board_name(self.platform.board_name_file),
                read_board_revision(self.platform.revision_file),
                read_board_serial_number(self.platform.serial_number_file))
        except AttributeError as e:
            print(e)

    def _load_pins(self, header):
        """
        Load pin_desc and create Pin instance for the given header
        :param header: pin header to load (P8 or P9)
        :return: Pin instance generator
        """
        if header is Header.p8:
            definitions = BBB_P8_DEF
        elif header is Header.p9:
            definitions = BBB_P9_DEF
        else:
            return None

        for pin_def in definitions:
            pin_def['header'] = header
            yield Pin(self, pin_def)

    def iter_p8_pins(self):
        """
        Iterates on P8 header pins
        :return: iterator on P8 header pins
        """
        yield self.iter_pins(Header.p8)

    def iter_p9_pins(self):
        """
        Iterates on P9 header pins
        :return: iterator on P8 header pins
        """
        yield self.iter_pins(Header.p9)

    def iter_pins(self, header=None, driver_pin=None, address=None):
        """
        Iter pins matching criterias (AND)
        :param header: pin header
        :param driver_pin: driver pin
        :param address: pin address
        :return: iteretor on pin matching given criterias
        """
        for pin in self.pins:
            if header is not None and pin.header != header:
                continue
            if driver_pin is not None and pin.driver_pin != driver_pin:
                continue
            if address is not None and pin.address != address:
                continue
            yield pin

    def get_pin(self, header=None, driver_pin=None, address=None):
        """
        Get first pin match the given criterias
        :param header: pin header
        :param driver_pin: driver pin
        :param address: pin address
        :return: first pin matching criterias
        """
        try:
            iterator = self.iter_pins(header, driver_pin, address)
            return next(iterator)
        except Exception as e:
            LOGGER.debug("No pin matching args header='%s', driver_pin='%s', address='0x%x'" % (header, driver_pin, address))

    @asyncio.coroutine
    def _update_from_pinctrl(self):
        """
        Update bord pins configuration from pinctrl files informations
        :return:
        """
        pins_file_content = yield from read_pins_file(self.platform.pins_file)
        for pins_line in pins_file_content:
            if pins_line is not None:
                #look for pin matching the driver pin
                pin = self.get_pin(address=pins_line['address'])
                if pin is not None:
                    pin.update_from_pins(pins_line)
                else:
                    LOGGER.debug("No pin definition matching address '0x%x' from 'pins' file was not found" % pins_line['address'])
        pinmux_pins_file_content = yield from read_pinmux_pins(self.platform.pinmux_pins_file)
        for pinmux_pins_line in pinmux_pins_file_content:
            #look for pin matching the driver pin
            if pinmux_pins_line is not None:
                pin = self.get_pin(address=pinmux_pins_line['address'])
                if pin is not None:
                    pin.update_from_pinmux_pins(pinmux_pins_line)
                else:
                    LOGGER.debug("No pin definition matching address '0x%x' from 'pinmux-pins' was not found" % pinmux_pins_line['address'])

    def __repr__(self):
        return "Board(name=%r,revision=%r,serial_number=%r)" % \
               (self.name,
                self.revision,
                self.serial_number)
