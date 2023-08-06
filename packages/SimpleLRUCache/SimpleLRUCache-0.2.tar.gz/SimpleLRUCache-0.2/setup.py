#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages


setup(name='SimpleLRUCache',
      version='0.2',
      description="""Simple LRU cache for python. Provides a dictionary-like, forgetful object.""",
      author='Johannes Buchner, Chris Stucchio',
      author_email='buchner.johannes@gmx.at',
      license='Dual: GPL v3 or BSD',
      url='https://github.com/JohannesBuchner/SimpleLRUCache',
      packages = ['simplelrucache'],
     )
