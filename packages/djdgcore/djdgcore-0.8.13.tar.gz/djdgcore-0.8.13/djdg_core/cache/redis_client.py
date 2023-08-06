#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2016/7/12
 """
from __future__ import unicode_literals, absolute_import
from django.conf import settings
from redis import StrictRedis
import re


class MyStrictRedis(StrictRedis):
    """
    copy from o2o.cache to use REDIS.
    REDIS代理，将用到KEYS方法的KEY放入一个SET，使用KEYS操作时在此SET中查找
    """
    key_patterns = ('.*:column:map:set', '.*:groupon:set',
                    '.*:region:.*:promotion:set', 'seckill:.*',
                    '.*:seckill:set', 'smscode:.*', 'group:buying:*')

    def get_pattern_key(self, key):
        """
        """
        for pattern in self.key_patterns:
            if re.match(pattern, key):
                return pattern
        return None

    def keys(self, pattern='*'):
        pattern_key = self.get_pattern_key(pattern)
        if pattern_key is None:
            return ()

        result = []
        pattern = pattern.replace('*', '.*')
        keys = self.smembers(pattern_key)
        if keys is None:
            return ()
        for key in keys:
            if re.match(pattern, key):
                result.append(key)

        return result

    def add_key(self, key):
        pattern_key = self.get_pattern_key(key)
        if pattern_key is not None:
            super(MyStrictRedis, self).sadd(pattern_key, key)

    def remove_key(self, key):
        pattern_key = self.get_pattern_key(key)
        # print pattern_key,key
        if pattern_key is not None:
            self.srem(pattern_key, key)

    def brpoplpush(self, listname, back_list):
        darr = super(MyStrictRedis, self).brpop(listname)
        if darr is None:
            return None
        data = darr[1]
        super(MyStrictRedis, self).lpush(back_list, data)
        return data

    def execute_command(self, *args, **options):
        try:
            return super(MyStrictRedis, self).execute_command(*args, **options)
        except Exception as e:
            print e.message
            pass

    def clean_keys(self, pattern_key):
        if pattern_key in self.key_patterns:
            names = super(MyStrictRedis, self).smembers(pattern_key)
            if not names:
                names = set()
            names.add(pattern_key)
            super(MyStrictRedis, self).delete(*names)

    def delete(self, *names):
        for name in names:
            self.remove_key(name)
        return super(MyStrictRedis, self).delete(*names)

    def hset(self, name, key, value):
        self.add_key(name)
        return super(MyStrictRedis, self).hset(name, key, value)

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        self.add_key(name)
        return super(MyStrictRedis, self).set(name, value, ex, px, nx, xx)

    def rpush(self, name, *values):
        self.add_key(name)
        return super(MyStrictRedis, self).rpush(name, *values)

    def lpush(self, name, *values):
        self.add_key(name)
        return super(MyStrictRedis, self).lpush(name, *values)

    def sadd(self, name, *values):
        # log.info(name)
        self.add_key(name)
        return super(MyStrictRedis, self).sadd(name, *values)


class DefaultCacheProxy(object):
    """
    Proxy access to the default Cache object's attributes.

    This allows the legacy `cache` object to be thread-safe using the new
    ``caches`` API.
    """
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if not self._client:
            kwargs = {}
            for k, v in settings.REDIS.items():
                kwargs[k.lower()] = v
            self._client = MyStrictRedis(**kwargs)
        return self._client

    def __getattr__(self, name):
        return getattr(self.client, name)


cache = DefaultCacheProxy()
