import asyncio
import logging
import re
from enum import Enum
from pybone.pin_desc import BBB_P8_DEF, BBB_P9_DEF, BBB_control_module_addr
from pybone.utils import filesystem

LOGGER = logging.getLogger(__name__)

_board_name_file_pattern = '/sys/devices/bone_capemgr.*/baseboard/board-name'
_revision_file_pattern = '/sys/devices/bone_capemgr.*/baseboard/revision'
_serial_number_file_pattern = '/sys/devices/bone_capemgr.*/baseboard/serial-number'
_pins_file_pattern = '/sys/kernel/debug/pinctrl/44e10800.pinmux/pins'

loop = asyncio.get_event_loop()


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


def parse_pinmux_line(line):
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
        LOGGER.warning("Failed parsing '%s'." % line, e)
        return None


@asyncio.coroutine
def read_pinmux(pins_file):
    file_content = yield from filesystem.read_async(pins_file)
    if file_content is not None:
        for line in file_content[1:]:
            yield parse_pinmux_line(line)

@asyncio.coroutine
def read_board_name(board_file):
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
    return boardname

@asyncio.coroutine
def read_board_revision(revision_file):
    file_content = yield from filesystem.read_async(revision_file)
    if file_content is None:
        return None
    else:
        return file_content[0].strip()

@asyncio.coroutine
def read_board_serial_number(serial_number_file):
    file_content = yield from filesystem.read_async(serial_number_file)
    if file_content is None:
        return None
    else:
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

    def update_from_pinmux(self, pinmux_info):
        if self.address == pinmux_info['address']:
            self.register_mode = pinmux_info['reg']['mode']
            self.register_slew = pinmux_info['reg']['slew']
            self.register_receive = pinmux_info['reg']['receive']
            self.register_pull = pinmux_info['reg']['pull']
            self.register_pulltype = pinmux_info['reg']['pulltype']
        else:
            LOGGER.fatal("Pin address configuration '0x%x' doesn't match pinmux address '0x%x" % (self.address, pinmux_info['address']))


    @property
    def address(self):
        if self.reg_offset is not None:
            return Board.pin_reg_address + self.reg_offset
        else:
            return 0

    @property
    def key(self):
        return "%s_%d" % (self.header.value, self.header_pin)



class Board(object):
    pin_reg_address = 0x44e10000
    def __init__(self, run_platform):
        self.platform = run_platform
        loop.run_until_complete(self._init_async())
        self.pins = [pin for pin in self._load_pins(Header.p8)]
        self.pins += [pin for pin in self._load_pins(Header.p9)]
        loop.run_until_complete(self._update_from_pinmux())

    @asyncio.coroutine
    def _init_async(self):
        self.name = yield from read_board_name(self.platform.board_name_file)
        self.revision = yield from read_board_revision(self.platform.revision_file)
        self.serial_number = yield from read_board_serial_number(self.platform.serial_number_file)

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
            print(e)

    @asyncio.coroutine
    def _update_from_pinmux(self):
        """
        Update bord pins configuration from pinmux files informations
        :return:
        """
        for pinmux in read_pinmux(self.platform.pins_file):
            #look for pin matching the driver pin
            pin = self.get_pin(address=pinmux['address'])
            if pin is not None:
                pin.update_from_pinmux(pinmux)
            #else:
            #    LOGGER.warning("No pin definition matching address '0x%x' from pinmux was not found" % pinmux['address'])