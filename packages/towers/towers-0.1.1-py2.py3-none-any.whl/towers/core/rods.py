#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# @module towers.core.rods
# @version 0.1
# @copyright (c) 2017-present Francis Horsman.

import copy
import json
from collections import Sequence, namedtuple

import six

from .disk import Disk
from .errors import InvalidRod, InvalidRodHeight
from .rod import Rod
from .utils import Serializable
from .validation import Validatable, validate_height

__all__ = ['Rods']


class Rods(namedtuple('Rods', ('start', 'end', 'tmp')), Sequence, Validatable, Serializable):
    """
    A collection of 3 Rod's that form the Tower.

    :param Rod start:
        The rod containing the disks at their start position.
    :param Rod end:
        The rod containing the disks at their end position.
    :param Rod tmp:
        The intermediary rod.
    :param int height:
        The height of the tower.
    :raises InvalidTowerHeight:
        The height of the tower is invalid.
    :raises InvalidRod:
        A rod is not of expected type `Rod`.
    :raises InvalidRodHeight:
        A rod height is inconsistent with the specified height.
    :raises DuplicateDisk:
        A rod contains a duplicate disk
    :raises CorruptRod:
        A disk is on top of a disk of smaller size on a Rod.
    """

    def __new__(cls, height=1, start=None, end=None, tmp=None):
        validate_height(height)

        start_rod = [Disk(rod, height) for rod in range(height)]

        for rod in [start, end, tmp]:
            if rod is None:
                continue
            if not isinstance(rod, Rod):
                raise InvalidRod(rod)
            elif rod.height != height:
                raise InvalidRodHeight(rod, height)
            rod.validate()

        if start is None:
            start = Rod(
                name='start',
                disks=start_rod,
                height=height,
            )
        if end is None:
            end = Rod(
                name='end',
                height=height,
            )
        if tmp is None:
            tmp = Rod(
                name='tmp',
                height=height,
            )

        self = super(Rods, cls).__new__(cls, start, end, tmp)
        self._height = height
        return self

    def to_json(self):
        """
        Return a json serializable representation of this instance.

        :rtype:
            object
        """
        return {
            'height': self.height,
            'start': self.start.to_json(),
            'end': self.end.to_json(),
            'tmp': self.tmp.to_json(),
        }

    @classmethod
    def from_json(cls, d):
        """
        Return a class instance from a json serializable representation.

        :param str|dict d:
            The json or decoded-json from which to create a new instance.
        :rtype:
            :class:`Rods`
        :raises:
            See :class:`Rods`.__new__.
        """
        if isinstance(d, six.string_types):
            d = json.loads(d)
        return cls(
            height=d.pop('height'),
            start=Rod.from_json(d.pop('start')),
            end=Rod.from_json(d.pop('end')),
            tmp=Rod.from_json(d.pop('tmp')),
        )

    @property
    def height(self):
        """
        Retrieve the height of the rods (ie: max number of disks each one can hold).

        :rtype:
            int
        """
        return self._height

    def __copy__(self):
        """
        Return a shallow copy of this instance.

        :rtype:
            Rods
        """
        return Rods(
            height=self.height,
            start=copy.copy(self.start),
            end=copy.copy(self.end),
            tmp=copy.copy(self.tmp),
        )

    def __deepcopy__(self, *a):
        """
        Return a deep copy of this instance.

        :rtype:
            Rods
        """
        return Rods(
            height=self.height,
            start=copy.deepcopy(self.start),
            end=copy.deepcopy(self.end),
            tmp=copy.deepcopy(self.tmp),
        )

    def __eq__(self, other):
        """
        Compare Rods instances for equivalence.

        :param Rods other:
            The other Rods to compare.
        :rtype: bool
        """
        if isinstance(other, Rods):
            if all([getattr(self, field) == getattr(other, field) for field in self._fields]):
                return True

    def __str__(self):
        return 'Rods({height} - {start}, {end}, {tmp})'.format(
            height=self.height,
            start=self.start,
            end=self.end,
            tmp=self.tmp,
        )

    def __bool__(self):
        """
        A Rods is considered True if it contains any disks on any rods.

        :rtype:
            bool
        """
        return self.__nonzero__()

    def __nonzero__(self):
        """
        A Rods is considered non-zero if it contains any disks on any rods.

        :rtype:
            bool
        """
        return any([bool(i) for i in self])

    def __len__(self):
        """
        Obtain the number of Rods.

        :rtype:
            int
        """
        return len(self._fields)

    def __iter__(self):
        """
        Iterate over all the rods.

        :rtype:
            Rod
        """
        for name in self._fields:
            yield getattr(self, name)

    def validate(self):
        """
        Perform self validation.

        :raises DuplicateDisk:
            This rod already contains this disk
        :raises CorruptRod:
            A disk is on top of a disk of smaller size.
        """
        for rod in self:
            rod.validate()
