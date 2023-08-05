#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

setup(
    name='wclog',
    version='0.1.1',
    description=(
        'wechat controller: client part'
    ),
    long_description=open('README.txt').read(),
    author='zhoulinjun',
    author_email='zhoulinjun1994@163.com',
    maintainer='zhoulinjun',
    maintainer_email='zhoulinjun1994@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='http://github.com/zhoulinjun1994',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
