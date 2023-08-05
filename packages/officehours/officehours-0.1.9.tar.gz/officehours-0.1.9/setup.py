#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def version():
    init = path.join(path.dirname(__file__), 'officehours', '__init__.py')
    line = list(filter(lambda l: l.startswith('__version__'), open(init)))[0]
    return line.split('=')[-1].strip(" '\"\n")


setup(
    name='officehours',
    packages=['officehours'],
    version=version(),
    description='Utility to calculate time intervals in working hours',
    author='Guillermo Guirao Aguilar',
    author_email='contact@guillermoguiraoaguilar.com',
    url='https://github.com/Funk66/officehours.git',
    keywords=['time', 'hours', 'office', 'business', 'work'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ]
)
