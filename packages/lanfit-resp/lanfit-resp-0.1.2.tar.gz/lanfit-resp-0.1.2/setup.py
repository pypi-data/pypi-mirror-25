#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='lanfit-resp',
    version='0.1.2',
    description='requests to flask response with Link header.',
    long_description=read('README.rst'),
    author='ll1l11',
    author_email='ll1l11@qq.com',
    url='',
    license='MIT',
    py_modules=['lanfit_resp'],
    install_requires=['Flask', 'lanfit-exceptions'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)
