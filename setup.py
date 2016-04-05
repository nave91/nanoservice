#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='nanoservice',
      version='0.1',
      description='Python nanoservice to hold objects in memory.',
      author='Naveen Lekkalapudi',
      author_email='rekojtoor@gmail.com',
      url='https://www.github.com/nave91/nanoservice',
      packages=find_packages(),
      scripts=['nanoservice/bin/nanoservicectl'],
      install_requires=[
          'psutil>=4.1.0',
      ],
     )