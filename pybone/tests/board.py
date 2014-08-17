import os
import unittest
from pybone.config import Config
from pybone.board import *
from pybone import pin_desc


class ParsePinMuxTestFunction(unittest.TestCase):

    def init_board(self):
        pf = Config('system_name', 'kernel_release', 'processor')
        pf.board_name_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/board-name")
        pf.revision_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/revision")
        pf.serial_number_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/serial-number")
        pf.pins_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/pins")
        pf.pinmux_pins_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/pinmux-pins")
        return Board(pf)

    def test_parse_pins_line(self):
        line = "pin 0 (44e10800) 00000031 pinctrl-single"
        pin = parse_pins_line(line)
        self.assertEqual(0, pin['index'])
        self.assertEqual(0x44e10800, pin['address'])
        self.assertEqual( (0x31 & 0x07), pin['reg']['mode'])
        self.assertEqual(RegSlew.fast, pin['reg']['slew'])
        self.assertEqual( RegPull.disabled, pin['reg']['pull'])
        self.assertEqual( RegPullType.pullup, pin['reg']['pulltype'])

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

    def test_Board(self):
        board = self.init_board()
        self.assertIsNotNone(board)
        self.assertEquals(board.name, 'BeagleBone Black')
        self.assertEquals(board.revision, '0A6A')
        self.assertEquals(board.serial_number, '0414BBBK2885')

    def test_pin_key(self):
        """
        Test pin key attributes match Header_PinNumber, like P8_3
        """
        board = self.init_board()

        p_def = pin_desc.BBB_P8_DEF[2]
        p_def['header'] = Header.p8
        p = Pin(board, p_def)
        self.assertEquals('P8_3', p.key)

if __name__ == '__main__':
    unittest.main()


