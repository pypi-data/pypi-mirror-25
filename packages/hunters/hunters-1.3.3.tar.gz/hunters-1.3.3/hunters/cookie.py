# -*- coding:utf-8 -*-
# Created by qinwei on 2017/9/8
import json


class CookieStore(object):
    """爬虫会话保持"""

    def set(self, key, val):
        pass

    def get(self, key):
        pass


class MemoryCookieStore(CookieStore):
    """内存型的Session"""
    data_container = {}

    def set(self, key, val):
        self.data_container[key] = val

    def get(self, key):
        return self.data_container.get(key)


class RedisCookieStore(CookieStore):
    """"""

    def __init__(self, redis):
        """

        :param redis: redis instance
        """
        self.redis = redis

    def get(self, key):
        data = self.redis.get(self._get_key(key))
        if not data:
            return {}
        return json.loads(data)

    def set(self, key, val):
        #: 所有的Cookie都一个小时过期
        self.redis.setex(self._get_key(key), json.dumps(val, ensure_ascii=False), 3600)

    def _get_key(self, key):
        return "s:hunter-cookie:" + key
