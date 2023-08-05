#!/usr/bin/env python
# -*- coding: latin-1 -*-
#   ______
#  /\__  _\
#  \/_/\ \/   ___   __  __  __    __  _ __  ____
#     \ \ \  / __`\/\ \/\ \/\ \ /'__`/\`'__/',__\
#      \ \ \/\ \L\ \ \ \_/ \_/ /\  __\ \ \/\__, `\
#       \ \_\ \____/\ \___x___/\ \____\ \_\/\____/
#        \/_/\/___/  \/__//__/  \/____/\/_/\/___/
#
#

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

if sys.version_info[0] == 2:
    if sys.version_info[1] < 6:
        raise ValueError('Only compatible with python; >= 2.6')

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'towers', '__version__.py')) as f:
    exec (f.read(), about)

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    version = about['__version__']
    print("Tagging release as: {v}".format(v=version))
    os.system("git tag -a {v} -m 'version {v}'".format(v=version))
    os.system('git push --tags')
    os.system('python setup.py bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()
elif sys.argv[-1] == 'test':
    os.system('make test')
    sys.exit()

requires = [
    'six',
    'pip',
    'enum34',
]

setup_requirements = [
    'nose',
]
test_requirements = [
    'nose',
    'nose-cov',
]

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=find_packages(include=['towers']),
    # package_data={
    #     'requirements': ['requirements/*.txt'],
    # },
    include_package_data=True,
    license=about['__license__'],
    requires=requires,
    install_requires=requires,
    zip_safe=False,
    keywords='towers',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
