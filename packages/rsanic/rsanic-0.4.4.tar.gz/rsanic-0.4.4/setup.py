#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: mehmet@mkorkmaz.com
# last_updated: 2017-02-14

import os
from setuptools import setup, find_packages
from rsanic import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

readme = read('README.rst')
changelog = read('ChangeLog.rst')


setup(
    name='rsanic',
    version=__version__,
    author='Mehmet Korkmaz',
    author_email='mehmet@mkorkmaz.com',
    packages=find_packages(),
    install_requires=[
        'sanic==0.5.4',
        'sanic_session==0.1.2',
        'jinja2==2.9.5'
    ],
    description='Micro framework built on top of sanic.py written in Python 3.',
    long_description=readme + '\n' + changelog,
    license='https://opensource.org/licenses/MIT',
    url='https://github.com/reformo/rsanic',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet',
    ],
)
