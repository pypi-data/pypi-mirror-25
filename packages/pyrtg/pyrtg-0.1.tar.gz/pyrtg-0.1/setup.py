# -*- coding: utf-8 -*-

# Learn more: https://github.com/jonpurdy/pyrtg

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyrtg',
    version='0.1',
    description='Classes for easily generating PRTG XML output.',
    long_description=readme,
    author='Jon Purdy',
    author_email='jon@jonpurdy.com',
    url='https://github.com/jonpurdy/pyrtg',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
