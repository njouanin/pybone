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

from .pin_desc import BBB_P8_DEF, BBB_P9_DEF
from .pin import Pin


LOGGER = logging.getLogger(__name__)


class Header(Enum):
    p8 = 'P8'
    p9 = 'P9'
    board = 'board'


class Board(object):

    def __init__(self, runtime_platform, loop=None):
        self.platform = runtime_platform
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop
        (self.name, self.revision, self.serial_number) = self.platform.read_board_info(loop)
        self.pins = [pin for pin in self._load_pins(Header.p8)]
        self.pins += [pin for pin in self._load_pins(Header.p9)]
        self.update_pins_runtime_attributes()

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

    def update_pins_runtime_attributes(self, loop=None):
        """
        Update bord pins runtime configuration from pinctrl files informations
        :return:
        """
        import itertools

        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

        (pins_array, pinsmux_array) = self._loop.run_until_complete(
            asyncio.gather(self.platform.read_pins_file(),
                           self.platform.read_pinmux_pins()))

        if pins_array is None and pinsmux_array is None:
            LOGGER.warn("Platform didn't provide pins runtime informations")
        else:
            for attributes in itertools.chain(pins_array, pinsmux_array):
                if attributes is not None:
                    #look for pin matching the driver pin
                    pin = self.get_pin(address=attributes['address'])
                    if pin is not None:
                        pin.update_runtime(attributes)
                    else:
                        LOGGER.debug("No pin definition matching address '0x%x' from 'pins' file was not found" % pins_line['address'])

    def __repr__(self):
        return "Board(name=%r,revision=%r,serial_number=%r)" % \
               (self.name,
                self.revision,
                self.serial_number)
