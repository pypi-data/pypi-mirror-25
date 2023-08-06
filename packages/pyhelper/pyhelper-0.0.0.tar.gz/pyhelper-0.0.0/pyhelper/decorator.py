# coding=utf-8

import time
import random
import functools


def sleep_call(key, min_ms, max_ms):
    """
    限制调用时间间隔，即保证两次调用之间至少间隔了min毫秒
    :param key: 标识
    :param min_ms: 最小间隔(毫秒)
    :param max_ms: 最大间隔(毫秒)
    :return:
    """

    def wrapper(func):
        cache = {}

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if key in cache.keys():
                (result, updateTime) = cache[key]
                expires = random.randint(min_ms, max_ms)  # 有效期(毫秒)
                sleep_ms = expires - (time.time() - updateTime) * 1000
                if sleep_ms > 0:
                    time.sleep(sleep_ms * 0.001)

            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result

        return wrapped

    return wrapper
