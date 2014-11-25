# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='Manage',
    version='0.1',
    py_modules=['manage'],
    include_package_data=True,
    install_requires=required,
    entry_points='''
        [console_scripts]
        rethinkdb_cli=manage:rethinkdb_cli
        docs_cli=manage:docs_cli
    ''',
)

