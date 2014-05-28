import asyncio
from pybone.bone import Board

VERSION = (0, 0, 1, 'alpha', 0)


def _checkRequirements():
    #Check python >= 3.4
    import sys
    if sys.version_info < (3, 4):
        raise ImportError("Python 3.4 or more is required")

    #Check root or sudoers


_checkRequirements()


#setup version
from pybone._version import get_pretty_version
__version__ = get_pretty_version(VERSION)
