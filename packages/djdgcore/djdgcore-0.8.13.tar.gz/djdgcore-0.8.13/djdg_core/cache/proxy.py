#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2016/10/29
 """
from __future__ import unicode_literals, absolute_import
from djdg_core.cache.redis_client import cache
from djdg_core.exceptions import TimeOutError
import time


class CacheProxy(object):
    """
    缓存代理
    """
    FORMAT = None
    LOCK_PREFIX = 'lock'
    LOCK_EXPIRE = 300
    KEY_EXPIRE = None
    WAIT_INTERVAL = 1

    def __init__(self, engine=None, **kwargs):
        if not engine:
            engine = cache
        self.logger = kwargs.pop('logger', None)
        self.__engine = engine
        self.__kwargs = kwargs
        self.__key = None
        self.__lock_key = None

    def __getattr__(self, item):
        if item.startswith('hook_'):
            item = item[5:]

            def wrapper(*args, **kwargs):
                return self.hook(item, *args, **kwargs)
            return wrapper
        return getattr(self.__engine, item)

    def hook(self, func, *args, **kwargs):
        """
        统一通过管道方式执行命令
        :param func:
        :param args:
        :param kwargs:
        :return:
        """
        expire = kwargs.pop('expire', None)
        pipe = self.__engine.pipeline()
        call_func = getattr(pipe, func)
        pipe = call_func(self.key, *args, **kwargs)
        if expire and self.KEY_EXPIRE:
            pipe = pipe.expire(self.key, self.KEY_EXPIRE)
        r = pipe.execute()
        return r[0]

    @property
    def formatter(self):
        fmts = []
        for s in self.__class__.__mro__:
            fmt = getattr(s, 'FORMAT', None)
            if fmt:
                fmts.append(fmt)
        fmts.reverse()
        return ':'.join(fmts)

    @property
    def key(self):
        if not self.__key:
            self.__key = self.formatter.format(**self.__kwargs)
        return self.__key

    @property
    def lock_key(self):
        if not self.__lock_key:
            self.__lock_key = ':'.join([self.key, self.LOCK_PREFIX])
        return self.__lock_key

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def acquire(self):
        start = time.time()
        while True:
            nt = time.time()
            r = self.__engine.setnx(self.lock_key, nt)
            if r:
                break
            # 查看是否有丢弃的lock
            v = self.__engine.get(self.lock_key)
            if v:
                fv = float(v)
                if nt - fv > self.LOCK_EXPIRE:
                    v2 = self.__engine.getset(self.lock_key, nt)
                    if v == v2:
                        break
            # 检查是否超时
            if nt - start > self.LOCK_EXPIRE:
                raise TimeOutError('获取锁{}超时！'.format(self.lock_key))
            time.sleep(self.WAIT_INTERVAL)
            if self.logger:
                self.logger.info('getting {} lock, wait {}'.format(self.key, time.time() - nt))

    def release(self):
        """
        acquire保证同时只有一个客户端获得锁，因此这里直接删除
        :return:
        """
        self.__engine.delete(self.lock_key)
