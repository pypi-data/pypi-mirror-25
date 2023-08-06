#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='cpuspinner',
    packages=['cpuspinner'],
    version='0.1',
    description='A background thread spinning your cpu at 100%',
    author='Alex Newman',
    author_email='posix4e@gmail.com',
    url='https://github.com/posix4e/cpuspinner',
    keywords=['testing'],
    scripts=['bin/spin.py'])
