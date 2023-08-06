#!/usr/bin/env python
# Copyright 2017 Transwarp Inc. All rights reserved.
from setuptools import setup, find_packages

setup(
    name='libappadapter',
    version='0.2.7',
    description='An abstraction of applications converted from python APi to kubernetes templates',
    packages=find_packages(),
    include_package_data=True,
    url='http://172.16.1.41:10080/TDC/libappadapter.git',
    license='Transwarp Copyright',
    author='Transwarp',
    author_email='',
    install_requires=[
        'jsonnet==0.9.4',
        'PyYAML==3.12'
    ]
)
