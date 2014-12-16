# !/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='Manage',
    version='0.1',
    py_modules=['manage'],
    install_requires=[
        'click',
        'Pycco',
        'rethinkdb',
        'subprocess32',
        'tornado'
        ],
    entry_points='''
        [console_scripts]
        manage=manage:manage
    ''',
)
