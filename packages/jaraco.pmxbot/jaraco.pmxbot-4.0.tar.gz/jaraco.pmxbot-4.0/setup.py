#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
	long_description = readme.read()

name = 'jaraco.pmxbot'
description = 'pmxbot commands by jaraco'
nspkg_technique = 'managed'
"""
Does this package use "native" namespace packages or
pkg_resources "managed" namespace packages?
"""

params = dict(
	name=name,
	use_scm_version=True,
	author="Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	description=description or name,
	long_description=long_description,
	url="https://github.com/jaraco/" + name,
	packages=setuptools.find_packages(exclude='tests'),
	include_package_data=True,
	namespace_packages=(
		name.split('.')[:-1] if nspkg_technique == 'managed'
		else []
	),
	python_requires='>=2.7',
	install_requires=[
		'twilio>=6',
		'cherrypy_cors',
		'jaraco.itertools',
	],
	extras_require={
		'testing': [
			'pytest>=2.8',
			'pytest-sugar',
			'pmxbot',
			'cherrypy[testing]',
		],
		'docs': [
			'sphinx',
			'jaraco.packaging>=3.2',
			'rst.linker>=1.9',
		],
	},
	setup_requires=[
		'setuptools_scm>=1.15.0',
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
	],
	entry_points={
		'pmxbot_handlers': [
			'jaraco.pmxbot = jaraco.pmxbot',
			'http API = jaraco.pmxbot.http',
			'notification = jaraco.pmxbot.notification',
		],
	},
)
if __name__ == '__main__':
	setuptools.setup(**params)
