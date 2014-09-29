import unittest
import os
from unittest.mock import patch
from unittest.mock import MagicMock
from pybone.bone import Linux38Platform, PlatformError
from pybone.bone.linux_3_8.platform import get_board_name
from pybone.bone.linux_3_8.pinctrl import parse_pinmux_pins_file, parse_pins_line
from pybone.bone.pin import RegSlewEnum, RegPullEnum, RegPullTypeEnum


class Linux38PlatformTest(unittest.TestCase):
    _TEST_BOARD_NAME_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../resources/board-name")
    _TEST_REVISION_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../resources/revision")
    _TEST_SERIAL_NUMBER_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../resources/serial-number")
    _TEST_PINS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../resources/pins")
    _TEST_PINMUX_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../resources/pinmux-pins")

    def test_get_board_name(self):
        self.assertEquals('BeagleBone', get_board_name('A335BONE'))
        self.assertEquals('BeagleBone Black', get_board_name('A335BNLT'))
        self.assertIsNone(get_board_name('Something'))

    @patch('pybone.bone.platform.platform')
    def test_init_platform(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Linux')
        mock_platform.release = MagicMock(return_value='3.8')
        mock_platform.processor = MagicMock(return_value='arm')
        Linux38Platform()

    @patch('pybone.bone.platform.platform')
    def test_init_platform_fail_system(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Windows')
        mock_platform.release = MagicMock(return_value='3.8')
        mock_platform.processor = MagicMock(return_value='arm')
        with self.assertRaises(PlatformError):
            Linux38Platform()

    @patch('pybone.bone.platform.platform')
    def test_init_platform_fail_release(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Linux')
        mock_platform.release = MagicMock(return_value='2.6')
        mock_platform.processor = MagicMock(return_value='arm')
        with self.assertRaises(PlatformError):
            Linux38Platform()

    @patch('pybone.bone.platform.platform')
    def test_init_platform_fail_processor(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Linux')
        mock_platform.release = MagicMock(return_value='3.8')
        mock_platform.processor = MagicMock(return_value='intel')
        with self.assertRaises(PlatformError):
            Linux38Platform()

    @patch('pybone.bone.platform.platform')
    @patch.object(Linux38Platform, '_BOARD_NAME_FILE', _TEST_BOARD_NAME_FILE)
    @patch.object(Linux38Platform, '_REVISION_FILE', _TEST_REVISION_FILE)
    @patch.object(Linux38Platform, '_SERIAL_NUMBER_FILE', _TEST_SERIAL_NUMBER_FILE)
    @patch.object(Linux38Platform, '_PINS_FILE', _TEST_PINS_FILE)
    @patch.object(Linux38Platform, '_PINMUX_FILE', _TEST_PINMUX_FILE)
    def test_init_platform_files(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Linux')
        mock_platform.release = MagicMock(return_value='3.8')
        mock_platform.processor = MagicMock(return_value='arm')
        pf = Linux38Platform()
        self.assertEquals(pf.board_name_file, Linux38PlatformTest._TEST_BOARD_NAME_FILE)
        self.assertEquals(pf.revision_file, Linux38PlatformTest._TEST_REVISION_FILE)
        self.assertEquals(pf.serial_number_file, Linux38PlatformTest._TEST_SERIAL_NUMBER_FILE)
        self.assertEquals(pf.pins_file, Linux38PlatformTest._TEST_PINS_FILE)
        self.assertEquals(pf.pinmux_pins_file, Linux38PlatformTest._TEST_PINMUX_FILE)

    @patch('pybone.bone.platform.platform')
    @patch.object(Linux38Platform, '_BOARD_NAME_FILE', _TEST_BOARD_NAME_FILE)
    @patch.object(Linux38Platform, '_REVISION_FILE', _TEST_REVISION_FILE)
    @patch.object(Linux38Platform, '_SERIAL_NUMBER_FILE', _TEST_SERIAL_NUMBER_FILE)
    @patch.object(Linux38Platform, '_PINS_FILE', _TEST_PINS_FILE)
    @patch.object(Linux38Platform, '_PINMUX_FILE', _TEST_PINMUX_FILE)
    def test_platform_read_board_info(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Linux')
        mock_platform.release = MagicMock(return_value='3.8')
        mock_platform.processor = MagicMock(return_value='arm')
        pf = Linux38Platform()
        (board_name, board_revision, board_serial_number) = pf.read_board_info()
        self.assertEquals(board_name, 'BeagleBone Black')
        self.assertEquals(board_revision, '0A6A')
        self.assertEquals(board_serial_number, '0414BBBK2885')

    @patch('pybone.bone.platform.platform')
    @patch.object(Linux38Platform, '_BOARD_NAME_FILE', 'FAIL')
    @patch.object(Linux38Platform, '_REVISION_FILE', _TEST_REVISION_FILE)
    @patch.object(Linux38Platform, '_SERIAL_NUMBER_FILE', _TEST_SERIAL_NUMBER_FILE)
    @patch.object(Linux38Platform, '_PINS_FILE', _TEST_PINS_FILE)
    @patch.object(Linux38Platform, '_PINMUX_FILE', _TEST_PINMUX_FILE)
    def test_platform_read_board_info_fails(self, mock_platform):
        mock_platform.system = MagicMock(return_value='Linux')
        mock_platform.release = MagicMock(return_value='3.8')
        mock_platform.processor = MagicMock(return_value='arm')
        pf = Linux38Platform()
        with self.assertRaises(PlatformError):
            pf.read_board_info()

    def test_parse_pins_line(self):
        line = "pin 0 (44e10800) 00000031 pinctrl-single"
        pin = parse_pins_line(line)
        self.assertEqual(0, pin['index'])
        self.assertEqual(0x44e10800, pin['address'])
        self.assertEqual( (0x31 & 0x07), pin['reg']['mode'])
        self.assertEqual(RegSlewEnum.fast, pin['reg']['slew'])
        self.assertEqual( RegPullEnum.disabled, pin['reg']['pull'])
        self.assertEqual( RegPullTypeEnum.pullup, pin['reg']['pulltype'])

    def test_parse_pinmux_pins_line(self):
        line = "pin 0 (44e10800): mmc.10 (GPIO UNCLAIMED) function pinmux_emmc2_pins group pinmux_emmc2_pins"
        pin = parse_pinmux_pins_file(line)
        self.assertEqual(0, pin['index'])
        self.assertEqual(0x44e10800, pin['address'])
        self.assertEqual('mmc.10', pin['mux_owner'])
        self.assertEqual(None, pin['gpio_owner'])
        self.assertEqual('pinmux_emmc2_pins', pin['function'])
        self.assertEqual('pinmux_emmc2_pins', pin['group'])

    def test_parse_pinmux_pins_line2(self):
        line = "pin 0 (44e10800): (MUX UNCLAIMED) (GPIO UNCLAIMED)"
        pin = parse_pinmux_pins_file(line)
        self.assertEqual(0, pin['index'])
        self.assertEqual(0x44e10800, pin['address'])
        self.assertEqual(None, pin['mux_owner'])
        self.assertEqual(None, pin['gpio_owner'])
        self.assertEqual(None, pin['function'])
        self.assertEqual(None, pin['group'])

    def test_parse_pinmux_pins_line3(self):
        line = "pin 0 (44e10800): (MUX UNCLAIMED) gpio.test function gpio_pins group gpio_pins"
        pin = parse_pinmux_pins_file(line)
        self.assertEqual(0, pin['index'])
        self.assertEqual(0x44e10800, pin['address'])
        self.assertEqual(None, pin['mux_owner'])
        self.assertEqual('gpio.test', pin['gpio_owner'])
        self.assertEqual('gpio_pins', pin['function'])
        self.assertEqual('gpio_pins', pin['group'])
