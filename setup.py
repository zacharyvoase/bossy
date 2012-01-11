#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
import os.path as p

VERSION = open(p.join(p.dirname(p.abspath(__file__)), 'VERSION')).read().strip()

setup(
    name='bossy',
    version=VERSION,
    description='Write commands in Python, run them from the shell.',
    author='Zachary Voase',
    author_email='z@zacharyvoase.com',
    url='http://github.com/zacharyvoase/bossy',
    packages=find_packages(where='lib'),
    package_dir={'': 'lib'},
    entry_points={
        'console_scripts': [
            'boss = bossy.main:main',
        ],
    },
    install_requires=[
        'argparse>=1.2.1',
        'nose>=1.1.2',
    ],
)
