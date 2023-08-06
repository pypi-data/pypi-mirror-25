#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# @module towers.core.rod
# @version 0.1
# @copyright (c) 2017-present Francis Horsman.

import json
from collections import Iterable, Sized, namedtuple

import six

from .disk import Disk
from .errors import CorruptRod, DuplicateDisk
from .utils import Serializable
from .validation import Validatable

__all__ = ['Rod']


class Rod(
    namedtuple('Rod', ('name', 'disks', 'height')), Iterable, Sized, Validatable, Serializable
):
    """
    A single tower containing disks.
    """

    def __new__(cls, name, disks=None, height=0):
        """
        :param str name:
            The name of the rod.
        :param List[Disk] disks:
            (optional) mutatable list of `Disks`.
        :param int height:
            The height of the rod.
        :rtype: Rod
        :raises: See `Rod.validate`.
        """
        self = super(Rod, cls).__new__(cls, name, disks or [], height)
        self.validate()
        return self

    def to_json(self):
        """
        Return a json serializable representation of this instance.

        :rtype: object
        """
        return {
            'name': self.name,
            'height': self.height,
            'disks': [i.to_json() for i in self.disks],
        }

    @classmethod
    def from_json(cls, d):
        """
        Return a class instance from a json serializable representation.

        :param Union[str,dict] d:
            The json or decoded-json from which to create a new instance.
        :rtype: Rod
        :raises: See `Rod.__new__`.
        """
        if isinstance(d, six.string_types):
            d = json.loads(d)
        return cls(
            name=d.pop('name'),
            height=d.pop('height'),
            disks=[Disk.from_json(i) for i in d.pop('disks')],
        )

    def __len__(self):
        return self.height

    def __copy__(self):
        """
        Return a shallow copy of this instance.

        :rtype: Rod
        """
        return Rod(
            self.name,
            disks=self.disks,
            height=self.height,
        )

    def __deepcopy__(self, *d):
        """
        Return a deep copy of this instance.

        :param dict d:
            Memoisation dict.
        :rtype: Rod
        """
        return Rod(
            self.name,
            disks=self.disks[:],
            height=self.height,
        )

    def __str__(self):
        return '{name}({rod})'.format(
            name=self.name,
            rod=self.disks,
        )

    def __eq__(self, other):
        """
        Compare Rod instances for equivalence.

        :param Rod other:
        :rtype: bool
        """
        if isinstance(other, Rod):
            if other.height == self.height:
                if other.disks == self.disks:
                    return True

    def __bool__(self):
        """
        A Rod is considered True if it contains any disks.

        :rtype: bool
        """
        return self.__nonzero__()

    def __nonzero__(self):
        """
        A Rod is considered non-zero if it contains any disks.

        :rtype: bool
        """
        return bool(self.disks)

    def pop(self):
        """
        Pop the top most disk from this rod and return it

        :rtype: Disk
        """
        return self.disks.pop()

    def append(self, disk, validate=True):
        """
        Append the disk to this rod and optionally validate.

        :param Disk disk:
            The disk to add to the top of our rod.
        :param bool validate:
            True=perform self validation.
        """
        self.disks.append(disk)
        if validate:
            self.validate()

    def __iter__(self):
        """
        Iterate over all the disks in this rod.

        :rtype: Disk
        """
        for disk in self.disks:
            yield disk

    def validate(self):
        """
        Perform self validation.

        :raises DuplicateDisk:
            This rod already contains this disk
        :raises CorruptRod:
            A disk is on top of a disk of smaller size.
        :raises InvalidTowerHeight:
            The height of the tower is invalid.
        :raises InvalidDiskPosition:
            The position of the disk is invalid.
        """
        width = 0
        seen = set()

        for disk in reversed(list(iter(self))):
            disk_width = disk.width
            if disk_width in seen:
                raise DuplicateDisk(self, disk_width)
            seen.update([disk_width])

            if disk.width < width:
                raise CorruptRod(self, disk)
            width = disk_width

            disk.validate()
