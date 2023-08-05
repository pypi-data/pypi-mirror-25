#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 下午4:58
# @Author  : Hou Rong
# @Site    : 
# @File    : simple_redis.py
# @Software: PyCharm
import time


class SimpleRedis(object):
    def __init__(self, redis_conn, key):
        self.redis_conn = redis_conn
        self.key = key

    @property
    def last(self):
        return float(self.redis_conn.get(self.key) or -1.0)

    def set_new(self):
        return self.redis_conn.set(self.key, time.time())

    def lock(self):
        return self.redis_conn.lock(self.key)
