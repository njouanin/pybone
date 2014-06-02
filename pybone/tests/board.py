import os
import unittest
from pybone.platform import Platform
from pybone.board import *
from pybone import pin_desc


class ParsePinMuxTestFunction(unittest.TestCase):

    def init_board(self):
        pf = Platform('system_name', 'kernel_release', 'processor')
        pf.board_name_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/board-name")
        pf.revision_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/revision")
        pf.serial_number_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/serial-number")
        pf.pins_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/pins")
        return Board(pf)

    def test_parse_pinmux_line(self):
        line = "pin 0 (44e10800) 00000031 pinctrl-single"
        pin = parse_pinmux_line(line)
        self.assertEqual(0, pin['index'])
        self.assertEqual(0x44e10800, pin['address'])
        self.assertEqual( (0x31 & 0x07), pin['reg']['mode'])
        self.assertEqual(RegSlew.fast, pin['reg']['slew'])
        self.assertEqual( RegPull.disabled, pin['reg']['pull'])
        self.assertEqual( RegPullType.pullup, pin['reg']['pulltype'])

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


