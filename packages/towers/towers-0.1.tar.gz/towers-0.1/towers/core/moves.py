# !/usr/bin/env python
# -*- coding: latin-1 -*-
#
# @module towers.core.moves
# @version 0.1
# @copyright (c) 2017-present Francis Horsman.

from collections import namedtuple

__all__ = [
    'Move',
]


class Move(namedtuple('Move', ('disk', 'start', 'end', 'moves'))):
    """
    :param Disk disk:
        The disk that will be moved.
    :param Rod start:
        The state of the start_rod prior to the move.
    :param Rod end:
        The state of the end_rod prior to the move.
    :param int moves:
        The number of moves prior to the move.
    """

    def __new__(cls, disk, start, end, moves):
        return super(Move, cls).__new__(cls, disk, start, end, moves)
