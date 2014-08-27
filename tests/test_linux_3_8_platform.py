import unittest
import os
from unittest.mock import patch
from unittest.mock import MagicMock
from pybone.bone import Linux38Platform, PlatformError
from pybone.bone.linux_3_8 import get_board_name

class Linux38PlatformTest(unittest.TestCase):
    _TEST_BOARD_NAME_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/board-name")
    _TEST_REVISION_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/revision")
    _TEST_SERIAL_NUMBER_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/serial-number")
    _TEST_PINS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/pins")
    _TEST_PINMUX_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/pinmux-pins")

    def test_get_board_name(self):
        self.assertEquals('BeagleBone', get_board_name('A335BONE'))
        self.assertEquals('BeagleBone Black', get_board_name('A335BNLT'))
        self.assertIsNone(get_board_name('Something'))

    @patch('pybone.bone.platform')
    def test_init_platform(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Linux')
        mock_platform.release = MagicMock(return_value='3.8')
        mock_platform.processor = MagicMock(return_value='arm')
        Linux38Platform()

    @patch('pybone.bone.platform')
    def test_init_platform_fail_system(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Windows')
        mock_platform.release = MagicMock(return_value='3.8')
        mock_platform.processor = MagicMock(return_value='arm')
        with self.assertRaises(PlatformError):
            Linux38Platform()

    @patch('pybone.bone.platform')
    def test_init_platform_fail_release(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Linux')
        mock_platform.release = MagicMock(return_value='2.6')
        mock_platform.processor = MagicMock(return_value='arm')
        with self.assertRaises(PlatformError):
            Linux38Platform()

    @patch('pybone.bone.platform')
    def test_init_platform_fail_processor(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Linux')
        mock_platform.release = MagicMock(return_value='3.8')
        mock_platform.processor = MagicMock(return_value='intel')
        with self.assertRaises(PlatformError):
            Linux38Platform()

    @patch('pybone.bone.platform')
    @patch.object(Linux38Platform, '_BOARD_NAME_FILE', _TEST_BOARD_NAME_FILE)
    @patch.object(Linux38Platform, '_REVISION_FILE', _TEST_REVISION_FILE)
    @patch.object(Linux38Platform, '_SERIAL_NUMBER_FILE',_TEST_SERIAL_NUMBER_FILE)
    @patch.object(Linux38Platform, '_PINS_FILE', _TEST_PINS_FILE)
    @patch.object(Linux38Platform, '_PINMUX_FILE', _TEST_PINMUX_FILE)
    def test_platform_read_board_info(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Linux')
        mock_platform.release = MagicMock(return_value='3.8')
        mock_platform.processor = MagicMock(return_value='arm')
        pf = Linux38Platform()
        self.assertEquals(pf.board_name_file, Linux38PlatformTest._TEST_BOARD_NAME_FILE)
        self.assertEquals(pf.revision_file, Linux38PlatformTest._TEST_REVISION_FILE)
        self.assertEquals(pf.serial_number_file, Linux38PlatformTest._TEST_SERIAL_NUMBER_FILE)
        self.assertEquals(pf.pins_file, Linux38PlatformTest._TEST_PINS_FILE)
        self.assertEquals(pf.pinmux_pins_file, Linux38PlatformTest._TEST_PINMUX_FILE)
