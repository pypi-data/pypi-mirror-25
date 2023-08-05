#!/usr/bin/env python

import os
import pkg_resources
import sys

from setuptools import setup


install_requires = [line.strip() for line in open("requirements.txt").readlines()]

setup(
	name='chainer_addons',
	version='0.1.2',
	description='Some addon scripts for the chainer framework',
	author='Dimitri Korsch',
	author_email='korschdima@gmail.com',
	# url='https://chainer.org/',
	license='MIT License',
	packages=[
		'chainer_addons',
		'chainer_addons.models',
		'chainer_addons.training',
		'chainer_addons.dataset',
		'chainer_addons.utils',
		'chainer_addons.links',
	],
	zip_safe=False,
	setup_requires=[],
	install_requires=install_requires,
	# tests_require=['mock', 'nose'],
)
