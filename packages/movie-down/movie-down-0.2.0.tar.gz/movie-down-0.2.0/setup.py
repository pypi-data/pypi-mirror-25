#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of movie-down.
# https://github.com/Akhail/movie-down

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Michel Betancourt <MichelBetancourt23@gmail.com>

from setuptools import setup, find_packages
from movie_down import __version__


setup(
    name='movie-down',
    version=__version__,
    description='Interface to database movie for download',
    keywords='movie cli download',
    author='Michel Betancourt',
    author_email='MichelBetancourt23@gmail.com',
    url='https://github.com/Akhail/movie-down',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'tebless', 'bs4', 'requests'
    ],
    extras_require={
        'tests': [
            'mock',
            'nose',
            'coverage',
            'yanc',
            'preggy',
            'tox',
            'ipdb',
            'coveralls',
            'sphinx',
        ],
    },
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
    entry_points={
        'console_scripts': [
            'mvdown=movie_down.movie_down:main'
        ],
    },
)
