#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# @module towers.core.disk
# @version 0.1
# @copyright (c) 2017-present Francis Horsman.

import json
from collections import namedtuple

import six

from .errors import InvalidDiskPosition
from .utils import Serializable
from .validation import Validatable, validate_height

__all__ = ['Disk']


class Disk(namedtuple('Disk', ('original_position', 'height')), Validatable, Serializable):
    """
    An immutable representation of a sized disk that sits on a `Rod`.
    """

    def __new__(cls, original_position, height=1):
        """
        :param int original_position:
            The position on the `Rod` that this disks originally sat.
            Zero = The bottom of the `Rod`.
        :param int height:
            The maximum position of this :class:`Disk` on a :class:`Rod`.
        :rtype:
            :class:`Disk`
        :raises InvalidTowerHeight:
            The height of the tower is invalid.
        :raises InvalidDiskPosition:
            The position of the disk is invalid.
        """
        self = super(Disk, cls).__new__(
            cls,
            original_position,
            height,
        )
        self.validate()
        return self

    def to_json(self):
        """
        Return a json serializable representation of this instance.

        :rtype:
            object
        """
        return {
            'original_position': self.original_position,
            'height': self.height,
        }

    @classmethod
    def from_json(cls, d):
        """
        Return a class instance from a json serializable representation.

        :param str|dict d:
            The json or decoded-json from which to create a new instance.
        :rtype:
            :class:`Disk`
        :raises:
            See :class:`Disk.__new__`.
        """
        if isinstance(d, six.string_types):
            d = json.loads(d)
        return cls(
            original_position=d.pop('original_position'),
            height=d.pop('height'),
        )

    @property
    def width(self):
        """
        Obtain the width of the disk

        :rtype: int
        """
        return self.height - self.original_position

    def validate(self):
        """
        Perform self validation

        :raises InvalidTowerHeight:
            The height of the tower is invalid.
        :raises InvalidDiskPosition:
            The position of the disk is invalid.
        """
        validate_height(self.height)
        if (self.original_position < 0) or (self.original_position >= self.height):
            raise InvalidDiskPosition(self.original_position, self.height)

    def __str__(self):
        return 'Disk({original_position})'.format(
            original_position=self.original_position)

    def __repr__(self):
        return '{original_position}'.format(
            original_position='*' * self.width)
