from setuptools import setup, find_packages # Always prefer setuptools over distutils
from codecs import open # To use a consistent encoding
from os import path
from pybone import version_info

setup(
  name = "pybone",
  version = version_info,
  description="Python library for managing beagleboard hardware I/O",
  url="https://github.com/njouanin/pybone",
  license='GPLv3',
  packages=find_packages(exclude=['tests']),
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.4',
    'Topic :: System :: Hardware :: Hardware Drivers',
    'Topic :: System :: Operating System Kernels :: Linux'
  ]
)
