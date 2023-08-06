#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2016/9/18
 """
from __future__ import unicode_literals, absolute_import
from rest_framework import serializers


class SimpleListSerializer(serializers.ListSerializer):
    """
    默认的ListSerializer update操作
    """
    def update(self, instance, validated_data):
        ist_map = {ist.id: ist for ist in instance}
        upd_set = set()
        ret = []
        for item in validated_data:
            if 'id' in item:
                upd_set.add(item['id'])
                # 更新现有数据
                ist = ist_map.get(item['id'], None)
                if ist:
                    ret.append(self.child.update(ist, item))
            else:
                # 创建新数据
                ret.append(self.child.create(item))
        # 删除数据
        ist_del = set(ist_map.keys()) - upd_set
        for ist_id in ist_del:
            ist = ist_map[ist_id]
            ist.delete()
        return ret
