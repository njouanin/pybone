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

from pybone.config import Config,ConfigError

__author__ = 'nico'

class Linux38Config(Config):
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
        super().__init__(system_name, kernel_release, processor)
        if 'Linux' not in self.system_name:
            raise ConfigError("Unexpected system name '%r'" % self.system_name)
        elif '3.8' not in self.kernel_release:
            raise ConfigError("Unexpected kernel release '%r'" % self.kernel_release)
        elif 'arm' not in self.processor:
            raise ConfigError("Unexpected processor '%r'" % self.processor)

        _loop.run_until_complete(self.__init_async())

    def __init_async(self):
        self.board_name_file = yield from find_first_file(Linux38Config._board_name_file_pattern)
        self.revision_file = yield from find_first_file(Linux38Config._revision_file_pattern)
        self.serial_number_file = yield from find_first_file(Linux38Config._serial_number_file_pattern)
        self.pins_file = yield from find_first_file(Linux38Config._pins_file_pattern)
        self.pinmux_pins_file = yield from find_first_file(Linux38Config._pinmux_pins_file_pattern)
