# -*- coding: utf-8 -*-

# Learn more: https://github.com/jonpurdy/pyrtg

from setuptools import setup, find_packages

setup(
    name='pyrtg',
    version='0.2',
    description='Classes for easily generating PRTG XML output.',
    long_description='Classes for easily generating PRTG XML output.',
    author='Jon Purdy',
    author_email='jon+pyrtg@jonpurdy.com',
    url='https://github.com/jonpurdy/pyrtg',
    license='GNU General Public License v3 (GPLv3)',
    packages=find_packages(exclude=('tests', 'docs'))
)
