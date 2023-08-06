#!/usr/bin/env python
#coding:utf-8
from setuptools import setup,find_packages

setup(
	name='MyDataFrame',
	version='1.0.0',
	description=('a distributed DataFrame Python package'),
	long_description=open('README.rst').read(),
	author='QY',
	author_email='1295143818@qq.com',
	maintainer='someone',
	maintainer_email='someone@163.com',
	license='BSD License',
	packages=find_packages(),
	platforms=["all"],
	url='https://github.com/castleon/MyDataFrame',
	install_requires=[
		'numpy',
		'pandas']
	#classifiers=[],
)
