# -*- coding: utf-8 -*-
# !/usr/bin/env python

from setuptools import setup, find_packages
from io import open


setup(
    name='rm-sdk',
    version='3.0.0',
    keywords=('rm', 'sdk', 'raring meerkat', 'traveloka'),
    description='Python SDK for Raring Meerkat',
    long_description=open("README.rst", encoding="utf-8").read(),
    license='BSD License',

    url='https://github.com/tvlk-data/rm-sdk',
    author='Ahmad Faiyaz',
    author_email='ahmad.faiyaz@traveloka.com',

    packages=find_packages(),
    include_package_data=True,
    install_requires=list(map(lambda x: x.replace('==', '>=') and x.rstrip('\n'), open("requirements.txt", encoding="utf-8").readlines())),

    tests_require=['nose', 'httmock'],
    test_suite='tests',
)