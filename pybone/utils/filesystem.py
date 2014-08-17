import asyncio
import logging
import glob

LOGGER = logging.getLogger(__name__)

@asyncio.coroutine
def read_async(file):
    """
    File reading coroutine
    """
    try:
        fp = open(file)
    except PermissionError:
        LOGGER.warning("Permission error while reading %s. Consider running as root or some sudoers." % file)
        return None
    else:
        return fp.readlines()


@asyncio.coroutine
def find_first_file(pattern):
    """
    Find first file matching a file pattern
    """
    return glob.iglob(pattern)[0]