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
from enum import Enum

from pybone.pin_desc import BBB_P8_DEF, BBB_P9_DEF
from pybone.bone.pin import Pin


LOGGER = logging.getLogger(__name__)


class Header(Enum):
    p8 = 'P8'
    p9 = 'P9'
    board = 'board'


class Board(object):

    def __init__(self, run_platform):
        self.platform = run_platform
        (self.name, self.revision, self.serial_number) = self.platform.read_board_info()
        self.pins = [pin for pin in self._load_pins(Header.p8)]
        self.pins += [pin for pin in self._load_pins(Header.p9)]
        self._init_from_pinctrl()

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
            return None

    def _init_from_pinctrl(self, loop=None):
        """
        Update bord pins configuration from pinctrl files informations
        :return:
        """
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

        (pins_array, pinsmux_array) = self._loop.run_until_complete(
            asyncio.gather(self.platform.read_pins_file(),
                           self.platform.read_pinmux_pins()))
        if pins_array is None:
            LOGGER.warn("Platform didn't provide any pins")
        else:
            for pins_line in pins_array:
                if pins_line is not None:
                    #look for pin matching the driver pin
                    pin = self.get_pin(address=pins_line['address'])
                    if pin is not None:
                        pin.update_from_pins(pins_line)
                    else:
                        LOGGER.debug("No pin definition matching address '0x%x' from 'pins' file was not found" % pins_line['address'])

        if pinsmux_array is None:
            LOGGER.warn("Platform didn't provide any pinsmux")
        else:
            for pinmux_pins_line in pinsmux_array:
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
