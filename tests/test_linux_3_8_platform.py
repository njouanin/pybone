import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from pybone.bone import Linux38Platform, PlatformError


class Linux38PlatformTest(unittest.TestCase):

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
