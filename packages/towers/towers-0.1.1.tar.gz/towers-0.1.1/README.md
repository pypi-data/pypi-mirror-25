#TOWERS of Hanoi for Python

[![Author](https://img.shields.io/badge/Author:%20francis%20horsman-Available-brightgreen.svg?style=plastic)](https://www.linkedin.com/in/francishorsman)

[![Build Status](https://travis-ci.org/sys-git/towers.svg?branch=master)](https://travis-ci.org/sys-git/towers)
[![Coverage Status](https://coveralls.io/repos/github/sys-git/towers/badge.svg)](https://coveralls.io/github/sys-git/towers)
[![Documentation Status](https://readthedocs.org/projects/towers/badge/?version=latest)](http://towers.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/towers.svg)](https://badge.fury.io/py/towers)
[![PyPI](https://img.shields.io/pypi/l/towers.svg)]()
[![PyPI](https://img.shields.io/pypi/wheel/towers.svg)]()
[![PyPI](https://img.shields.io/pypi/pyversions/towers.svg)]()
[![PyPI](https://img.shields.io/pypi/status/towers.svg)]()
[![Updates](https://pyup.io/repos/github/sys-git/towers/shield.svg)](https://pyup.io/repos/github/sys-git/towers/)
[![Python 3](https://pyup.io/repos/github/sys-git/towers/python-3-shield.svg)](https://pyup.io/repos/github/sys-git/towers/)

Towers of Hanoi algorithm in a useful form.

##Example
```python
    >>> tower = Towers(height=3)
    >>> print(tower)
    Towers(Rods(3 - start([***, **, *]), end([]), tmp([])))
```
```python
    >>> print('moves required: {moves}'.format(moves=tower.moves_for_height(height)))
    moves required: 7
```
```python
    >>> with tower:
    ...    for i in tower:
    ...        print(i)
    Move(disk=*, start=Rod(name='start', disks=[***, **, *], height=3), end=Rod(name='end', disks=[], height=3), moves=0)
    Move(disk=**, start=Rod(name='start', disks=[***, **], height=3), end=Rod(name='tmp', disks=[], height=3), moves=1)
    Move(disk=*, start=Rod(name='end', disks=[*], height=3), end=Rod(name='tmp', disks=[**], height=3), moves=2)
    Move(disk=***, start=Rod(name='start', disks=[***], height=3), end=Rod(name='end', disks=[], height=3), moves=3)
    Move(disk=*, start=Rod(name='tmp', disks=[**, *], height=3), end=Rod(name='start', disks=[], height=3), moves=4)
    Move(disk=**, start=Rod(name='tmp', disks=[**], height=3), end=Rod(name='end', disks=[***], height=3), moves=5)
    Move(disk=*, start=Rod(name='start', disks=[*], height=3), end=Rod(name='end', disks=[***, **], height=3), moves=6)
```
```python
    >>> print(tower)
    Towers(Rods(3 - start([]), end([***, **, *]), tmp([])))
```
```python
    >>> print('moves taken: {moves}'.format(moves=tower.moves))
    moves taken: 7
```
##To install

```
    $ pip install towers
```

##Build documentation

```
    $ make sphinx-html
```
