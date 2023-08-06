#!/usr/bin/env python
from setuptools import setup

from cache_expire import __version__

setup(
    name='cache-expire',
    version=__version__,
    description='Memoize decorator with expire timeout.',
    author='Kjwon15',
    url='https://github.com/kjwon15/cache-expire',
    py_modules=['cache_expire'],
)
