#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from setuptools import setup


def readme():
	with open('README.rst') as f:
		return f.read()


setup(name='jk_commentjson',
	version='0.2017.10.7',
	description='This is a JSON parsing module that can get along with comments in JSON files.',
	author='Jürgen Knauth',
	author_email='pubsrc@binary-overflow.de',
	license='Apache 2.0',
	url='https://github.com/jkpubsrc/python-module-jk-commentjson',
	download_url='https://github.com/jkpubsrc/python-module-jk-commentjson/tarball/0.2017.10.7',
	keywords=['json'],
	packages=['jk_commentjson'],
	install_requires=[
	],
	include_package_data=True,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python :: 3.5',
		'License :: OSI Approved :: Apache Software License'
	],
	long_description=readme(),
	zip_safe=False)

