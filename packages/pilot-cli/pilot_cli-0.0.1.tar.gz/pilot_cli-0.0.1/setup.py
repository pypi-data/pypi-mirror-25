#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pilot-cli.
# https://github.com/cgarciae/pilot-cli

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, cgarciae <cgarcia.e88@gmail.com>

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()



tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='pilot_cli',
    version = "0.0.1", #TODO: generalize
    description='an incredible python package',
    long_description='''
an incredible python package
''',
    keywords='',
    author='kiwi',
    author_email='cristian@kiwicampus.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires = required,
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            'pilot-cli=pilot_cli.cli:main',
        ],
    },
)
