#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# @module towers.core.towers
# @version 0.1
# @copyright (c) 2017-present Francis Horsman.

import contextlib
import copy
import json
import math
from collections import Sequence

import six

from .errors import (
    InvalidEndingConditions, InvalidStartingConditions,
)
from .moves import Move
from .rod import Rod
from .rods import Rods
from .utils import Serializable
from .validation import (
    Validatable, validate_height, validate_moves, validate_rods,
)

__all__ = [
    'Towers',
]


class Towers(Sequence, Validatable, Serializable):
    """
    A representation of the towers including all logic.
    """

    class JsonEncoder(json.JSONEncoder):
        def default(self, obj):  # pylint: disable=E0202
            if isinstance(obj, Towers):
                return obj.to_json()
            else:  # pragma: no cover
                return json.JSONEncoder.default(self, obj)

    def __init__(self, height=1, rods=None, moves=0, verbose=False):
        """
        :param int height:
            The height of the towers (ie: max number of disks each one rod can hold).
        :param Rods rods:
            An existing :class:`Rods` instance to use with this :class:`Towers` (the heights must
            match).
        :param int moves:
            The number of moves already taken.
        :param verbose:
            True=enable verbose logging mode.
        """
        validate_height(height)
        validate_rods(rods)
        validate_moves(moves)
        self._rods = rods if rods is not None else Rods(height)
        self._moves = moves
        self._verbose = bool(verbose)

    def to_json(self):
        """
        Return a json serializable representation of this instance.

        :rtype: object
        """
        return {
            'height': self.height,
            'verbose': self.verbose,
            'moves': self.moves,
            'rods': self._rods.to_json(),
        }

    @classmethod
    def from_json(cls, d):
        """
        Return a class instance from a json serializable representation.

        :param str|dict d:
            The json or decoded-json from which to create a new instance.
        :rtype:
            Towers
        :raises:
            See :class:`Towers`.__new__.
        """
        if isinstance(d, six.string_types):
            d = json.loads(d)
        return cls(
            height=d.pop('height'),
            verbose=d.pop('verbose'),
            moves=d.pop('moves'),
            rods=Rods.from_json(d.pop('rods')),
        )

    @contextlib.contextmanager
    def context(self, reset_on_success=True, reset_on_error=False):
        """
        Create a temp context for performing moves.
        The state of this instance will be reset at context exit.

        :param bool reset_on_success:
            Reset this instance's state on exit from the context if no error occurred.
            Default = True.
        :param bool reset_on_error:
            Reset this instance's state on exit from the context if an error occurred.
            Default = False.
        """
        self.validate_start()

        verbose = self.verbose
        moves = self.moves
        rods = self._rods.to_json()

        try:
            yield self
            self.validate_end()
        except Exception:
            # Error inside context or validation:
            if reset_on_error:
                self._verbose = verbose
                self._moves = moves
                self._rods = Rods.from_json(rods)
        else:
            if reset_on_success:
                self._verbose = verbose
                self._moves = moves
                self._rods = Rods.from_json(rods)

    def __bool__(self):
        """
        A Towers is considered True if it's state is completed.

        :rtype:
            bool
        """
        return self.__nonzero__()

    def __nonzero__(self):
        """
        A Towers is considered non-zero if it's state is completed.

        :rtype:
            bool
        """
        try:
            self.validate_end()
            return True
        except Exception:
            return False

    def __copy__(self):
        """
        Return a shallow copy of this instance.

        :rtype:
            :class:`Towers`
        """
        return Towers(
            height=self.height,
            rods=self._rods,
            moves=self.moves,
            verbose=self.verbose,
        )

    def __deepcopy__(self, *d):
        """
        Return a deep copy of this instance.

        :param dict d:
            Memoisation dict.
        :rtype:
            :class:`Towers`
        """
        return Towers.from_json(self.to_json())

    def __eq__(self, other):
        """
        Compare Towers instances for equivalence.

        :param Towers other:
            The other :class:`Towers` to compare.
        :rtype:
            bool
        """
        if isinstance(other, Towers):
            if other.height == self.height:
                if other._rods == self._rods:
                    return True

    def __getitem__(self, index):
        """
        Get the :class:`Rod` at the given index.

        :param int index:
            The index to get the :class:`Rod` at.
        :rtype:
            Rod
        """
        return self._rods[index]

    def __contains__(self, x):
        """
        Does this :class:`Towers` contain the given :class:`Rod`.

        :param Rod x:
            The :class:`Rod` to find.
        :rtype:
            bool
        """
        if isinstance(x, Rod):
            return x in self._rods

    def __len__(self):
        """
        Determine how many :class:`Rod`'s this :class:`Towers` contains.

        :rtype:
            int
        """
        return len(self._rods)

    def __iter__(self):
        """
        Run the towers, yielding :class:`Move` instances.
        """
        for i in self.move_tower(
            height=self.height,
            start=self.start_rod,
            end=self.end_rod,
            tmp=self.tmp_rod,
        ):
            yield i

    def __str__(self):
        return 'Towers({rods})'.format(rods=self._rods)

    @property
    def verbose(self):
        """
        Obtain this instance's verbose flag.

        :rtype:
            bool
        """
        return self._verbose

    @verbose.setter
    def verbose(self, verbose):
        """
        Set this instance's verbose flag

        :param object verbose:
            True=enable verbose logging mode.
        """
        self._verbose = bool(verbose)

    @property
    def moves(self):
        """
        Determine how many moves have occurred so far.

        :rtype:
            int
        """
        return self._moves

    @property
    def height(self):
        """
        Obtain the height of the :class:`Towers` (ie: max number of disks each one rod can hold).

        :rtype:
            int
        """
        return self._rods.height

    @staticmethod
    def moves_for_height(height):
        """
        Determine the max number of moves required to solve the puzzle for the given height

        :param int height:
            The height of the :class:`Rods` (number of :class:`Disk` on a :class:`Rod`).
        :rtype: int
        """
        return int(math.pow(2, height)) - 1

    def validate_start(self):
        """
        Validate the start conditions for this towers

        :raises InvalidTowerHeight:
            The height of the :class:`Towers` is invalid
        :raises DuplicateDisk:
            This :class:`Rod` already contains this :class:`Disk`.
        :raises CorruptRod:
            A :class:`Disk` is on top of a :class:`Disk` of smaller size.
        :raises InvalidStartingConditions:
            Initial conditions are invalid.
        """
        validate_height(self.height)
        self._rods.validate()

        if not (bool(self._rods.start) and not bool(self._rods.end)):
            raise InvalidStartingConditions(self._rods, self.moves)

        if self.moves != 0:
            raise InvalidStartingConditions(self._rods, self.moves)

    def validate_end(self):
        """
        Validate the end conditions for this towers.

        :raises InvalidTowerHeight:
            The height of the tower is invalid
        :raises DuplicateDisk:
            This :class:`Rod` already contains this :class:`Disk`.
        :raises CorruptRod:
            A :class:`Disk` is on top of a :class:`Disk` of smaller size.
        :raises InvalidEndingConditions:
            End conditions are invalid.
        """
        validate_height(self.height)
        self._rods.validate()

        if not (bool(self._rods.end) and not bool(self._rods.start)):
            raise InvalidEndingConditions(self._rods)

    def validate(self):
        """
        Perform self validation.

        :raises InvalidTowerHeight:
            The height of the tower is invalid
        :raises DuplicateDisk:
            This :class:`Rod` already contains this :class:`Disk`.
        :raises CorruptRod:
            A :class:`Disk` is on top of a :class:`Disk` of smaller size.
        """
        validate_height(self.height)
        self._rods.validate()

    def __enter__(self):
        """
        Context-Manager entry, validate our entry state for towers-start conditions.

        :raises:
            See :func:`Towers.validate_start`.
        """
        self.validate_start()

    def __exit__(self, *args, **kwargs):
        """
        Context-Manager exit, validate our exit state for towers-end conditions.

        :raises:
            See :func:`Towers.validate_end`.
        """
        self.validate_end()

    def __call__(self):
        """
        Run the towers. Convenience method.

        :raises:
            See :func:`Towers.move_tower`.
        """
        for i in self:
            if self.verbose:
                print(i)

    @property
    def start_rod(self):
        """
        Retrieve the start :class:`Rod` for this towers.

        :rtype:
            Rod
        """
        return self._rods.start

    @property
    def end_rod(self):
        """
        Retrieve the end :class:`Rod` for this towers.

        :rtype:
            Rod
        """
        return self._rods.end

    @property
    def tmp_rod(self):
        """
        Retrieve the temporary :class:`Rod` for this towers.

        :rtype:
            Rod
        """
        return self._rods.tmp

    def move_tower(self, height, start, end, tmp):
        """
        Move the stack of `Disks` on a `Rod`.

        :param int height:
            The height of the :class:`Disk` to move.
        :param Rod start:
            The :class:`Rod` to move the :class:`Disk` from.
        :param Rod end:
            The :class:`Rod` to move the :class:`Disk` to.
        :param Rod tmp:
            The intermediary :class:`Rod` to use when moving the :class:`Disk`.
        """
        if height >= 1:
            for i in self.move_tower(height - 1, start, tmp, end):
                yield i
            for i in self.move_disk(start, end):
                yield i
            for i in self.move_tower(height - 1, tmp, end, start):
                yield i
        elif height == 1:
            for i in self.move_disk(start, end):
                yield i

    def move_disk(self, start, end):
        """
        Move the `Disk` from one Rod to another.

        :note:
            Generator, yields `Move` instances.
        :param Rod start:
            The :class:`Rod` to remove the :class:`Disk` from.
        :param Rod end:
            The :class:`Rods` to move the :class:`Disk` to.
        """
        start_rod = copy.deepcopy(start)
        end_rod = copy.deepcopy(end)
        moves = self.moves

        disk = start.pop()

        move = Move(disk, start_rod, end_rod, moves)

        end.append(disk)
        self._moves += 1

        yield move
