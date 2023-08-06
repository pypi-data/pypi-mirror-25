#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2016/12/14
 """
from __future__ import unicode_literals, absolute_import
from djdg_core.cache.proxy import CacheProxy
from djdg_core import settings
from uuid import uuid1


token_settings = settings.cache_token_settings


class TokenCache(CacheProxy):
    """
    token在redis中的key
    """
    FORMAT = token_settings['FORMAT']
    KEY_EXPIRE = token_settings['EXPIRE']

    def __init__(self, token, engine=None):
        super(TokenCache, self).__init__(engine, token=token)
        self.settings = token_settings


def set_token(user_id):
    token = str(uuid1())
    token_cache = TokenCache(token=token)
    token_cache.hook_set(user_id, expire=True)
    return token


def get_user_id(token):
    """
    通过token获取user id
    :param token: uuid1 产生的内容
    :return:
    """
    token_cache = TokenCache(token=token)
    user_id = token_cache.hook_get()
    return int(user_id) if user_id else user_id
