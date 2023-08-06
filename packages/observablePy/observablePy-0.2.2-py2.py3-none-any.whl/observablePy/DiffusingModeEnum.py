#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum, unique


@unique
class diffusingModeEnum(Enum):
    unknown = 0
    element = 1
    elements = 2
