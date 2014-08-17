"""
Version information
"""
import asyncio
import os
import subprocess
import datetime

loop = asyncio.get_event_loop()

@asyncio.coroutine
def _get_git_changeset():
    """Returns a numeric identifier of the latest git changeset.

    The result is the UTC timestamp of the changeset in YYYYMMDDHHMMSS format.
    This value isn't guaranteed to be unique, but collisions are very unlikely,
    so it's sufficient for generating the development version numbers.
    """
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = yield from asyncio.create_subprocess_shell('git log --pretty=format:%ct --quiet -1 HEAD',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell=True, cwd=repo_dir, universal_newlines=False)
    (stdin, stderr) = yield from git_log.communicate()
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(stdin))
    except ValueError:
        return None
    return timestamp.strftime('%Y%m%d%H%M%S')


@asyncio.coroutine
def _get_version(version):
    "Returns a PEP 386-compliant version number from VERSION."

    # Bbuild the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    # | {a|b|c}N - for alpha, beta and rc releases

    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    sub = ''
    if version[3] == 'alpha' and version[4] == 0:
        changeset = yield from _get_git_changeset()
        if changeset:
            sub = '.dev%s' % changeset

    elif version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])

    return str(main + sub)


def get_pretty_version(v):
    pretty_version = loop.run_until_complete(_get_version(v))
    return pretty_version