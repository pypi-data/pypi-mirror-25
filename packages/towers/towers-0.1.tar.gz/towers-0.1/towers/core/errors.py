#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# @module towers.core.errors
# @version 0.1
# @copyright (c) 2017-present Francis Horsman.

__all__ = [
    'TowersError',
    'DuplicateDisk',
    'CorruptRod',
    'InvalidStartingConditions',
    'InvalidEndingConditions',
    'InvalidTowerHeight',
    'InvalidDiskPosition',
    'InvalidRod',
    'InvalidRodHeight',
    'InvalidRods',
    'InvalidMoves',
]


class TowersError(Exception):
    """
    Base class of all `towers` errors.
    """
    pass


class InvalidRod(TypeError, TowersError):
    def __init__(self, rod):
        """

        :param object rod:
            The :class:`Rod` which is invalid.
        """
        super(InvalidRod, self).__init__(
            'invalid rod: {rod}'.format(rod=rod))
        self.rod = rod


class InvalidRods(TypeError, TowersError):
    def __init__(self, rods):
        """
        :param object rods:
            The :class:`Rods` which are invalid
        """
        super(InvalidRods, self).__init__(
            'invalid rod: {rods}'.format(
                rods=rods))
        self.rods = rods


class InvalidRodHeight(ValueError, TowersError):
    def __init__(self, rod, max_height):
        """
        :param Rod rod:
            The :class:`Rod` which has an invalid height.
        :param int max_height:
            The max allowed height of the :class:`Rod`.
        """
        super(InvalidRodHeight, self).__init__(
            'invalid rod height: {rod} expecting: {height}.'.format(
                rod=rod, height=max_height))
        self.rod = rod
        self.height = max_height


class DuplicateDisk(ValueError, TowersError):
    """
    A duplicate disk was found on a tower.
    """

    def __init__(self, rod, disk_width):
        """
        :param Rod rod:
            The duplicate :class:`Rod`.
        :param int disk_width:
            The width of the :class:`Disk`.
        """
        super(DuplicateDisk, self).__init__(
            'Duplicate disk width found: {disk_width} in: {rod}'.format(
                disk_width=disk_width, rod=rod))
        self.rod = rod
        self.disk_width = disk_width


class CorruptRod(ValueError, TowersError):
    """
    A :class:`Rod` with an invalid stack of disks was found.
    """

    def __init__(self, rod, disk):
        """
        :param Rod rod:
            The :class:`Rod` which is corrupt.
        :param int disk:
            A :class:`Disk` which sits directly atop a smaller :class:`Disk`.
        """
        super(CorruptRod, self).__init__(
            'Corrupt rod, at least one disk is larger than the one below it: {rod}'.format(
                rod=rod))
        self.rod = rod
        self.disk = disk


class InvalidStartingConditions(ValueError, TowersError):
    """
    The :class:`Rods` for the towers are not in the correct starting state.
    """

    def __init__(self, rods, moves):
        """
        :param Rod rods:
            The :class:`Rod`'s.
        :param int moves:
            Total number of moves already made (should be zero).
        """
        super(InvalidStartingConditions, self).__init__(
            'Invalid starting condition for rods: {rods}, with existing moves: {moves}'.format(
                rods=rods, moves=moves))
        self.rods = rods
        self.moves = moves


class InvalidEndingConditions(ValueError, TowersError):
    """
    The :class:`Rod`'s for the towers are not in the correct ending state.
    """

    def __init__(self, rods):
        """
        :param Rod rods:
            The :class:`Rod`'s.
        """
        super(InvalidEndingConditions, self).__init__(
            'Invalid ending condition for rods: {rods}'.format(
                rods=rods))
        self.rods = rods


class InvalidTowerHeight(ValueError, TowersError):
    """
    The height of the :class:`Tower` is invalid.
    """

    def __init__(self, height):
        """
        :param int height:
            The invalid height.
        """
        super(InvalidTowerHeight, self).__init__(
            'Invalid tower height: {height}'.format(
                height=height))
        self.height = height


class InvalidDiskPosition(ValueError, TowersError):
    """
    The position of the :class:`Disk` is invalid.
    """

    def __init__(self, position, height):
        """
        :param int position:
            The invalid position on the :class:`Rod`.
        :param int height:
            The height.
        """
        super(InvalidDiskPosition, self).__init__(
            'Invalid disk position: {position} on Rod of height: {height}'.format(
                position=position, height=height))
        self.position = position
        self.height = height


class InvalidMoves(ValueError, TowersError):
    """
    An invalid number of moves.
    """

    def __init__(self, moves):
        """
        :param int moves:
            The invalid `moves`.
        """
        super(InvalidMoves, self).__init__(
            'Invalid moves: {moves}'.format(
                moves=moves))
        self.moves = moves
