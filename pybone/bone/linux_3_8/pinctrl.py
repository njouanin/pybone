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

import logging
import re
from pybone.bone.pin import RegPullEnum, RegPullTypeEnum, RegRcvEnum, RegSlewEnum

LOGGER = logging.getLogger(__name__)


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

