#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='Flask-Redis-Sentinel',
    py_modules=['flask_redis_sentinel'],
    version='2.0.1',
    install_requires=['Flask>=0.10.1', 'redis>=2.10.3', 'redis_sentinel_url>=1.0.0,<2.0.0', 'six'],
    description='Redis-Sentinel integration for Flask',
    long_description=read('README.rst'),
    url='https://github.com/exponea/flask-redis-sentinel',
    author='Martin Sucha',
    author_email='martin.sucha@exponea.com',
    license='Apache 2.0',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

