#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# @module towers.core.validation
# @version 0.1
# @copyright (c) 2017-present Francis Horsman.


import abc

import six

from .errors import InvalidMoves, InvalidRods, InvalidTowerHeight

__all__ = [
    'Validatable',
    'validate_height',
    'validate_rods',
    'validate_moves',
]


class Validatable(object):
    @abc.abstractmethod
    def validate(self):
        """
        Perform self validation
        """
        raise NotImplementedError()


def validate_height(height):
    """
    Validate the height of a :class:`Tower`s or :class:`Rod`.

    :param int height:
        The height to validate.
    :raises InvalidTowerHeight:
        The height of the :class:`Tower` is invalid.
    """
    if height < 1:
        raise InvalidTowerHeight(height)


def validate_rods(rods):
    """
    Validate the rods.

    :param List[Rod]|None rods:
        The :class:`Rod`'s to validate.
    :raises InvalidRods:
        expecting type :class:`Rods`.
    :raises DuplicateDisk:
        This :class:`Rod` already contains this :class:`Disk`
    :raises CorruptRod:
        A :class:`Disk` is on top of a :class:`Disk` of smaller size.
    """
    from towers import Rods

    if rods is not None:
        if not isinstance(rods, Rods):
            raise InvalidRods(rods)
        rods.validate()


def validate_moves(moves):
    """
    Validate the number of moves.

    :param int moves:
        The moves count to validate.
    :raises InvalidMoves:
        The number of moves is not an number or is less than zero.
    """
    if moves is not None:
        if not isinstance(moves, six.integer_types):
            raise InvalidMoves(moves)
        if moves < 0:
            raise InvalidMoves(moves)
