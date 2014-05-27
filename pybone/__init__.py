import asyncio
import pybone._version as version
from pybone.bone import Board

VERSION = (0, 0, 1, 'alpha', 0)

loop = asyncio.get_event_loop()

def get_pretty_version(v=None):
    if v is None:
        v = VERSION
    future_version = asyncio.Future()
    asyncio.Task(version._get_version(future_version, v))
    loop.run_until_complete(future_version)
    return future_version.result()











