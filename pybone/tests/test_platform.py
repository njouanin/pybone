__author__ = 'nico'

import unittest
from unittest.mock import patch
from pybone.bone import Platform

class PlatformTest(unittest.TestCase):

    @patch('pybone.bone.platform')
    def test_init_platform(self, mock_platform):
        p=Platform()
        mock_platform.system.assert_called_once_with()
        mock_platform.release.assert_called_once_with()
        mock_platform.processor.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()