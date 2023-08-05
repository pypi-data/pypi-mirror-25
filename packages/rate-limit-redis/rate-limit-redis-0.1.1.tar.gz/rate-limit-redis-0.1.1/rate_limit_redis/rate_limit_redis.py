#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/9/5 下午7:06
# @Author  : Hou Rong
# @Site    : 
# @File    : rate_limit_redis.py
# @Software: PyCharm
import time
import threading
import functools
import redis_lock

from logging import getLogger
from .simple_redis import SimpleRedis
from redis_lock import AlreadyAcquired

RETRY_TIMES = 10
WAIT_TIME = 1

logger = getLogger(__name__)


class TooManyRetry(Exception):
    def __repr__(self):
        return "Too Many Retry, Now Max Retry Times Is :{}".format(RETRY_TIMES)


class RateLimitRedis(object):
    def __init__(self, redis_conn, key, period=1.0, every=1.0):
        if period <= 0:
            raise ValueError('Period must be > 0')

        if every <= 0:
            raise ValueError('Every must be > 0')

        self.simple_redis = SimpleRedis(redis_conn, key)
        self.every = float(every)
        self.frequency = abs(every) / float(period)
        self.thread_lock = threading.Lock()
        self.redis_lock = redis_lock.Lock(redis_conn, key, expire=self.every)

    def __call__(self, f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            with self:
                return f(*args, **kwargs)

        return wrapped

    def __enter__(self):
        return self.update_status()

    def update_status(self, retry=0):
        try:
            with self.thread_lock:
                with self.redis_lock:
                    elapsed = time.time() - self.simple_redis.last
                    left_to_wait = self.frequency - elapsed
                    if left_to_wait > 0:
                        time.sleep(left_to_wait)
                    self.simple_redis.set_new()
                    return self
        except AlreadyAcquired as e:
            logger.info(e)
            time.sleep(WAIT_TIME)
            retry += 1
            if retry <= RETRY_TIMES:
                return self.update_status(retry=retry)
            else:
                raise TooManyRetry()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
