import asyncio
import platform
import glob
import os
import logging
import re
from pybone.pin_desc import BBB_P8_DEF, BBB_P9_DEF

LOGGER = logging.getLogger(__name__)
SYSFS = '/sys'

loop = asyncio.get_event_loop()


@asyncio.coroutine
def read_async(file):
    try:
        fp = open(file)
    except PermissionError:
        LOGGER.warning("Permission while reading %s. Consider running as root or some sudoers." % file)
        return "UNDEFINED"
    else:
        return fp.readlines()


def find_first_sysfsfile(pattern):
    if not os.path.isabs(pattern):
        path = os.path.join(SYSFS, pattern)
    else:
        path = pattern
    it = glob.iglob(path)
    try:
        return next(it)
    except StopIteration:
        return None


@asyncio.coroutine
def _read_async_info(future, sysfs_file):
    file = find_first_sysfsfile(sysfs_file)
    if file is None:
        LOGGER.warning("No file found matching pattern '%s'." % sysfs_file)
        return "UNDEFINED"
    file_content = yield from read_async(file)
    future.set_result(file_content[0].strip())


def get_board_info(board_name_file='devices/bone_capemgr.*/baseboard/board-name',
                   revision_file='devices/bone_capemgr.*/baseboard/revision',
                   serial_number_file='devices/bone_capemgr.*/baseboard/serial-number'):
    future_name = asyncio.Future()
    asyncio.Task(_read_async_info(future_name, board_name_file))
    loop.run_until_complete(future_name)

    future_revision = asyncio.Future()
    asyncio.Task(_read_async_info(future_revision, revision_file))
    loop.run_until_complete(future_name)

    future_serial = asyncio.Future()
    asyncio.Task(_read_async_info(future_serial, serial_number_file))
    loop.run_until_complete(future_serial)

    boardname = future_name.result()
    if boardname == 'A335BONE':
        boardname = 'BeagleBone'
    elif boardname == 'A335BNLT':
        boardname = 'BeagleBone Black'
    revision = future_revision.result()
    serial = future_serial.result()

    return boardname, revision, serial


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
        pin_reg = {}
        pin_reg['mode'] = reg & 0x07
        pin_reg['slew'] = 'slow' if (reg & 0x40) else 'fast'
        pin_reg['receive'] = 'enabled' if (reg & 0x20) else 'disabled'
        pin_reg['pull'] = 'enabled' if ((reg >> 3) & 0x01) else 'disabled'
        pin_reg['pulltype'] = 'pullup' if ((reg >> 4) & 0x01) else 'pulldown'

        return {'index': pin_index, 'address': pin_address, 'reg': pin_reg}
    except Exception as e:
        LOGGER.warning("Failed parsing '%s'." % line, e)
        return None


def parse_pinmux(pins_file='kernel/debug/pinctrl/44e10800.pinmux/pins'):
    f_pins = find_first_sysfsfile(pins_file)
    if f_pins is None:
        LOGGER.warning("No file found matching pattern 'kernel/debug/pinctrl/44e10800.pinmux/pins'.")
    else:
        lines = yield from read_async(f_pins)
        for line in lines[1:]:
            yield parse_pinmux_line(line)


class System(object):
    def __init__(self):
        self.machine = platform.machine()
        self.node = platform.node()
        self.platform = platform.platform()
        self.processor = platform.processor()
        self.system_release = platform.release()
        self.system_name = platform.system()

    def __repr__(self):
        return "Platform(machine=%r,node=%r,platform=%r,processor=%r,system_release=%r,system_name=%r)" % \
               (self.machine, self.node, self.platform, self.processor, self.system_release, self.system_name)


class Board(object):
    def __init__(self, pins_file=None, board_file_name=None, revision_file=None, serial_number_file=None):
        self.system = System()
        (self.board_name, self.board_revision, self.board_serial_number) = get_board_info(board_file_name, revision_file, serial_number_file)
        self.pins = BBB_P8_DEF.copy()
        self.pins.append(BBB_P9_DEF.copy())
        self._update_from_pinmux(pins_file)

    def _update_from_pinmux(self, pins_file=None):
        pinmux_info = list(parse_pinmux(pins_file))
        for pin in self.pins:
            pinmux = [item for item in pinmux_info if item['index'] == pin['driver_pin']]
            pin['current_conf'] = pinmux[0]