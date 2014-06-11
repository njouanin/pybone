import platform
import asyncio
from pybone.utils.filesystem import find_first_file

_loop = asyncio.get_event_loop()


class PlatformError(Exception):
    pass


class Platform(object):
    """
    Base class for platform definition
    This class should not
    """
    def __init__(self, system_name, kernel_release, processor):
        self.system_name = system_name
        self.kernel_release = kernel_release
        self.processor = processor

    def __repr__(self):
        return "%s(system_name=%r,kernel_release=%r,processor=%r)" % \
               (self.__class__.__name__,
                self.system_name,
                self.kernel_release,
                self.processor)


class Linux38BonePlatform(Platform):
    """
    Linux running on BeagleBone platform
    This should match the system configuration running on a beagleboard
    """
    _board_name_file_pattern = '/sys/devices/bone_capemgr.*/baseboard/board-name'
    _revision_file_pattern = '/sys/devices/bone_capemgr.*/baseboard/revision'
    _serial_number_file_pattern = '/sys/devices/bone_capemgr.*/baseboard/serial-number'
    _pins_file_pattern = '/sys/kernel/debug/pinctrl/44e10800.pinmux/pins'
    _pinmux_pins_file_pattern = '/sys/kernel/debug/pinctrl/44e10800.pinmux/pinmux-pins'

    def __init__(self, system_name, kernel_release, processor):
        super(Linux38BonePlatform, self).__init__(system_name, kernel_release, processor)
        if self.system_name != 'Linux':
            raise PlatformError("Unexpected system name '%r'" % self.system_name)
        elif not self.kernel_release.startswith('3.8'):
            raise PlatformError("Unexpected kernel release '%r'" % self.kernel_release)
        elif not self.processor.startswith('arm'):
            raise PlatformError("Unexpected processor '%r'" % self.processor)

        _loop.run_until_complete(self.__init_async())

    def __init_async(self):
        self.board_name_file = yield from find_first_file(Linux38BonePlatform._board_name_file_pattern)
        self.revision_file = yield from find_first_file(Linux38BonePlatform._revision_file_pattern)
        self.serial_number_file = yield from find_first_file(Linux38BonePlatform._serial_number_file_pattern)
        self.pins_file = yield from find_first_file(Linux38BonePlatform._pins_file_pattern)
        self.pinmux_pins_file = yield from find_first_file(Linux38BonePlatform._pinmux_pins_file_pattern)

local_system = platform.system()
local_release = platform.release()
local_processor = platform.processor()
try:
    local_platform = Linux38BonePlatform(local_system, local_release, local_processor)
except PlatformError:
    local_platform = Platform(local_system, local_release, local_processor)
