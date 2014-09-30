__author__ = 'nico'

import logging
from enum import Enum

LOGGER = logging.getLogger(__name__)

PIN_REG_ADDRESS = 0x44e10000


class RegSlewEnum(Enum):
    slow = 'slow'
    fast = 'fast'


class RegRcvEnum(Enum):
    enabled = 'enabled'
    disabled = 'disabled'


class RegPullEnum(Enum):
    enabled = 'enabled'
    disabled = 'disabled'


class RegPullTypeEnum(Enum):
    pullup = 'pullup'
    pulldown = 'pulldown'


class Pin(object):
    def __init__(self, board, definition):
        self.board = board
        #Pin static attributes
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
        #Pin runtime attributes
        self.register_mode = None
        self.register_slew = None
        self.register_receive = None
        self.register_pull = None
        self.register_pulltype = None
        self.mux_owner = None
        self.gpio_owner = None
        self.function = None
        self.group = None
        if self.reg_offset is not None:
            #reg_offset is None for non CPU pins
            self.address = PIN_REG_ADDRESS + self.reg_offset

    def update_runtime(self, attributes):
        if self.address == attributes['address']:
            if 'reg' in attributes:
                self.register_mode = attributes['reg']['mode']
                self.register_slew = attributes['reg']['slew']
                self.register_receive = attributes['reg']['receive']
                self.register_pull = attributes['reg']['pull']
                self.register_pulltype = attributes['reg']['pulltype']
            if 'mux_owner' in attributes:
                self.mux_owner = pinmux_info['mux_owner']
            if 'gpio_owner' in attributes:
                self.mux_owner = pinmux_info['gpio_owner']
            if 'function' in attributes:
                self.function = pinmux_info['function']
            if 'group' in attributes:
                self.group = pinmux_info['group']
        else:
            LOGGER.debug("Pin address configuration '0x%x' doesn't match pins address '0x%x" % (self.address, attributes['address']))

    @property
    def key(self):
        return "%s_%d" % (self.header.value, self.header_pin)

    def __repr__(self):
        sb = []
        for key in self.__dict__:
            sb.append("%r=%r" % (key, self.__dict__[key]))
        return "Pin(" + ','.join(sb) + ")"
