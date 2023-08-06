#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# @module towers
# @version 0.1
# @copyright (c) 2017-present Francis Horsman.
#
#   ______ _____   __      __  ____    ____    ____
#  /\__  _/\  __`\/\ \  __/\ \/\  _`\ /\  _`\ /\  _`\
#  \/_/\ \\ \ \/\ \ \ \/\ \ \ \ \ \L\_\ \ \L\ \ \,\L\_\
#     \ \ \\ \ \ \ \ \ \ \ \ \ \ \  _\L\ \ ,  /\/_\__ \
#      \ \ \\ \ \_\ \ \ \_/ \_\ \ \ \L\ \ \ \\ \ /\ \L\ \
#       \ \_\\ \_____\ `\___x___/\ \____/\ \_\ \_\ `\____\
#        \/_/ \/_____/'\/__//__/  \/___/  \/_/\/ /\/_____/
#
#

from .core.disk import Disk
from .core.errors import (
    CorruptRod, DuplicateDisk, InvalidDiskPosition, InvalidEndingConditions, InvalidMoves,
    InvalidRod, InvalidRodHeight, InvalidRods, InvalidStartingConditions, InvalidTowerHeight,
    TowersError,
)
from .core.moves import Move
from .core.rod import Rod
from .core.rods import Rods
from .core.towers import Towers
from .core.validation import validate_height, validate_moves, validate_rods
from .__version__ import __version__, __author__, __title__

__all__ = [
    'Towers',
    'Disk',
    'Rod',
    'Rods',
    'Move',
    'TowersError',
    'DuplicateDisk',
    'CorruptRod',
    'InvalidStartingConditions',
    'InvalidEndingConditions',
    'InvalidTowerHeight',
    'InvalidDiskPosition',
    'InvalidRod',
    'InvalidRods',
    'InvalidRodHeight',
    'InvalidMoves',
    'validate_height',
    'validate_rods',
    'validate_moves',
]
