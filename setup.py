#!/usr/bin/env python

import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='ranchy',
      description='Ranchy project will be able to collect data about a server farm',
      long_description=open('README.rst', 'r').read()
      author='Jeroen Op \'t Eynde',
      author_email='jeroen.opteynde@mobilevikings.com',
      url='http://github.com/Duologic/ranchy',
      packages=['ranchy'],)
