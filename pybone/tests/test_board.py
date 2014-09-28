import os
import unittest

from unittest.mock import MagicMock
from pybone.bone import Platform
from pybone.board import *
from pybone import pin_desc


class ParsePinMuxTestFunction(unittest.TestCase):

    def test_init_board_read_board_info(self):
        pf = Platform()
        pf.read_board_info = MagicMock(return_value=['BeagleBone Black', '0A6A', '0414BBBK2885'])
        board = Board(pf)
        self.assertIsNotNone(board)
        self.assertEquals(board.name, 'BeagleBone Black')
        self.assertEquals(board.revision, '0A6A')
        self.assertEquals(board.serial_number, '0414BBBK2885')

    # def test_pin_key(self):
    #     """
    #     Test pin key attributes match Header_PinNumber, like P8_3
    #     """
    #     board = self.init_board()
    #
    #     p_def = pin_desc.BBB_P8_DEF[2]
    #     p_def['header'] = Header.p8
    #     p = Pin(board, p_def)
    #     self.assertEquals('P8_3', p.key)

if __name__ == '__main__':
    unittest.main()


