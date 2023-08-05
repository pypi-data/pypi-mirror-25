#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(*paths):
    """ read files """
    with open(os.path.join(*paths), 'r') as filename:
        return filename.read()

setup(
    name="ced",
    version="0.1",
    description="A lightweight, cross-platform, no-dependency configuration editor.",
    long_description=(read('README.rst')),
    url="https://github.com/regisb/ced",
    license='MIT',
    author="Régis Behmo",
    author_email="nospam@behmo.com",
    packages=['ced'],
    package_data={
        'ced': ['ced'],
    },
    entry_points={
        'console_scripts': [
            'ced=ced:ced_module.main',
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
