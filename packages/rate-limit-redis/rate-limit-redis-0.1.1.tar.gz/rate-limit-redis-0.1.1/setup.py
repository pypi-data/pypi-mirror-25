#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 下午10:05
# @Author  : Hou Rong
# @Site    : 
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup, find_packages
from rate_limit_redis import __version__

setup(
    name='rate-limit-redis',
    version=__version__,
    license='MIT',
    description="A python rate limit tools, which have good compatibility for redis and gevent",
    author='Henry Hou',
    author_email='nmghr9@gmail.com',
    url='https://github.com/nmghr9/RateLimitRedis',
    install_requires=[
        'python-redis-lock',
    ],
    packages=find_packages(where='.', exclude=['']),
    test_utils='test',
    test_suite='test',
    zip_safe=False,
)
