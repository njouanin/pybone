import os
import unittest
import pybone.bone


class ParsePinMuxTestFunction(unittest.TestCase):

    def test_parse_pinmux_line(self):
        line = "pin 0 (44e10800) 00000031 pinctrl-single"
        pin = pybone.bone.parse_pinmux_line(line)
        self.assertEqual(0, pin['index'])
        self.assertEqual(0x44e10800, pin['address'])
        self.assertEqual( (0x31 & 0x07), pin['reg']['mode'])
        self.assertEqual( 'fast', pin['reg']['slew'])
        self.assertEqual( 'disabled', pin['reg']['pull'])
        self.assertEqual( 'pullup', pin['reg']['pulltype'])

    def test_parse_pin_mux(self):
        test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pins")
        pins_list = list(pybone.bone.parse_pinmux(test_file))
        self.assertIsNotNone(pins_list)
#        for info in pins_list :
#            print(info)
        self.assertEqual(142, len(pins_list))


    def test_Board(self):
        pins_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pins")
        board_name_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "board-name")
        revision_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "revision")
        serial_number_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "serial-number")
        board = pybone.bone.Board(pins_file, board_name_file, revision_file, serial_number_file)
        self.assertIsNotNone(board)

if __name__ == '__main__':
    unittest.main()


