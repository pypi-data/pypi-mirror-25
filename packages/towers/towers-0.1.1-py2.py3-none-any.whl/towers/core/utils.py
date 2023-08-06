#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# @module towers.core.utils
# @version 0.1
# @copyright (c) 2017-present Francis Horsman.

import abc


class Serializable(object):
    """
    A mixin which shows that a class is serializable.
    """

    @abc.abstractmethod
    def to_json(self):
        """
        Return a json serializable representation of this instance.

        :rtype: object
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def from_json(self, d):
        """
        Return a class instance from a json serializable representation.

        :param str|dict d:
            The json or decoded-json from which to create a new instance from.
        """
        raise NotImplementedError()
