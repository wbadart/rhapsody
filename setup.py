#!/usr/bin/env python3

from setuptools import find_packages, setup


setup(name='rhapsody',
      version='1.0.0a0',
      description='Next generation music recommendations',

      packages=find_packages(),
      url='https://wbadart.github.io/rhapsody',
      homepage='https://wbadart.github.io/rhapsody',

      install_requires=[
          'Django',
          'requests',
          'wbutil',
      ],

      zip_safe=False)
