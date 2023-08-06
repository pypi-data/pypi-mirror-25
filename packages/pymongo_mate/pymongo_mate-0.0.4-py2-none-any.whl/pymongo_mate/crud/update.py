#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
extend ``pymongo.Collection.update`` method.
"""

__all__ = [
    "upsert_many"
]


def upsert_many(col, data):
    """
    Only used when having "_id" field.

    **中文文档**

    要求 ``data`` 中的每一个 ``document`` 都必须有 ``_id`` 项。这样才能进行
    ``upsert`` 操作。
    """
    ready_to_insert = list()
    for doc in data:
        res = col.update({"_id": doc["_id"]}, {"$set": doc}, upsert=False)
        # 没有任何数据被修改, 且不是因为数据存在但值相同
        if res["nModified"] == 0 and res["updatedExisting"] is False:
            ready_to_insert.append(doc)
    col.insert(ready_to_insert)
