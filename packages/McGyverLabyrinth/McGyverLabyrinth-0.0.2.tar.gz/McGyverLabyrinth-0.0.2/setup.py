#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

import McGyverLabyrinth

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='McGyverLabyrinth',
	version='0.0.2',
	author='Ronan LE HAY',
	author_email='ronanlehay@gmail.com',
	url='https://github.com/NanroYahel/P3_Labyrinthe',
	packages=find_packages(),
	install_requires =required,
	long_description=open('README.md').read(),
	include_package_data=True)

