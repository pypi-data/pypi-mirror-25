#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.2.2'

setup(
    name='gwc',
    version=version,
    description='GeneDock command-line workflow client for interacting with GeneDock platform',
    # long_description=readme,
    packages=find_packages(),
    install_requires=['gdpy>=0.0.7.1', 'prettytable==0.7.2'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'gwc = gwc.gwc_scripts:main',
        ]
    },
    url="https://www.genedock.com",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
