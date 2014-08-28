__author__ = 'nico'

from enum import Enum


class RegSlewEnum(Enum):
    slow = 'slow'
    fast = 'fast'


class RegRcvEnum(Enum):
    enabled = 'enabled'
    disabled = 'disabled'


class RegPullEnum(Enum):
    enabled = 'enabled'
    disabled = 'disabled'


class RegPullTypeEnum(Enum):
    pullup = 'pullup'
    pulldown = 'pulldown'
