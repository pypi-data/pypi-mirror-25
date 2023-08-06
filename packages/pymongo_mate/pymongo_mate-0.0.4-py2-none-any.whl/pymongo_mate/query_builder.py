#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module helps user to build pymongo query dict.
"""

import re


class Logic(object):
    @staticmethod
    def and_(*filters):
        return {"$and": list(filters)}

    @staticmethod
    def or_(*filters):
        return {"$or": list(filters)}

    @staticmethod
    def nor(*filters):
        return {"$nor": list(filters)}

    @staticmethod
    def not_(expression):
        return {"$not": expression}


class Comparison(object):
    """``==``, ``!=``, ``>``, ``>=``, ``<``, ``<=``.
    """
    @staticmethod
    def less_than_equal(value):
        """
        ``<=``

        Example::

            filters = {field: Comparison.less_than_equal(10)}
        """
        return {"$lte": value}

    @staticmethod
    def less_than(value):
        """
        ``<``

        Example::

            filters = {field: Comparison.less_than(10)}
        """
        return {"$lt": value}

    @staticmethod
    def greater_than_equal(value):
        """
        ``>=``

        Example::

            filters = {field: Comparison.greater_than_equal(10)}
        """
        return {"$gte": value}

    @staticmethod
    def greater_than(value):
        """
        ``>``

        Example::

            filters = {field: Comparison.greater_than(10)}
        """
        return {"$gt": value}

    @staticmethod
    def equal_to(value):
        """
        ``==``

        Example::

            filters = {field: Comparison.equal_to(10)}
        """
        return {"$eq": value}

    @staticmethod
    def not_equal_to(value):
        """
        ``!=``

        Example::

            filters = {field: Comparison.not_equal_to(10)}
        """
        return {"$ne": value}


class Lang(object):
    """
    Language code Collection.
    """
    English = "en"
    French = "fr"
    German = "de"
    Italian = "it"
    Portuguese = "pt"
    Russian = "ru"
    Spanish = "es"
    SimplifiedChineses = "zhs"
    TraditionalChineses = "zht"


class Text(object):
    """Search text by:

    - startswith
    - endswith
    - contain sub string
    - full text serach
    """
    @staticmethod
    def startswith(text, ignore_case=True):
        """
        Test if a string-field start with ``text``.

        Example::

            filters = {"path": Text.startswith(r"C:\\")}
        """
        if ignore_case:
            compiled = re.compile(
                "^%s" % text.replace("\\", "\\\\"), re.IGNORECASE)
        else:  # pragma: no cover
            compiled = re.compile("^%s" % text.replace("\\", "\\\\"))

        return {"$regex": compiled}

    @staticmethod
    def endswith(text, ignore_case=True):
        """
        Test if a string-field end with ``text``.

        Example::

            filters = {"path": Text.endswith(".exe")}
        """
        if ignore_case:
            compiled = re.compile(
                "%s$" % text.replace("\\", "\\\\"), re.IGNORECASE)
        else:  # pragma: no cover
            compiled = re.compile("%s$" % text.replace("\\", "\\\\"))

        return {"$regex": compiled}

    @staticmethod
    def contains(text, ignore_case=True):
        """
        Test if a string-field has substring of ``text``.

        Example::

            filters = {"path": Text.contains("pymongo_mate")}
        """
        if ignore_case:
            compiled = re.compile(
                "%s" % text.replace("\\", "\\\\"), re.IGNORECASE)
        else:  # pragma: no cover
            compiled = re.compile("%s" % text.replace("\\", "\\\\"))

        return {"$regex": compiled}

    @staticmethod
    def fulltext(search, lang=Lang.English, ignore_case=True):
        """Full text search.

        Example::

            filters = Text.fulltext("python pymongo_mate")

        .. note::

            This field doesn't need to specify field.
        """
        return {
            "$text": {
                "$search": search,
                "$language": lang,
                "$caseSensitive": not ignore_case,
                "$diacriticSensitive": False,
            }
        }


class Array(object):
    """Array query builder.
    """
    @staticmethod
    def element_match(filters):
        """
        Test if any of items match the criterion.

        Example::

            data = [
                {"_id": 1, "results": [ 82, 85, 88 ]},
                {"_id": 2, "results": [ 75, 88, 89 ]},
            ]

            filters = {"results": {"$elemMatch": {"$gte": 80, "$lt": 85 }}}

            # equals to
            filters = {
                "results": Array.element_match({"$gte": 80, })
            }
        """
        return {"$elemMatch": filters}

    @staticmethod
    def include_all(items):
        """
        Test if an array-like field include all these items.

        Example::

            {"tag": ["a", "b", "c"]} include all ["a", "c"]
        """
        return {"$all": items}

    @staticmethod
    def include_any(items):
        """
        Test if an array-like field include any of these items.

        Example::

            {"tag": ["a", "b", "c"]} include any of ["c", "d"]
        """
        return {"$in": items}

    @staticmethod
    def exclude_all(items):
        """
        Test if an array-like field doesn't include any of these items.

        Example::

            {"tag": ["a", "b", "c"]} doesn't include any of ["d", "e"]
        """
        return {"$nin": items}

    @staticmethod
    def exclude_any(items):
        """
        Test if an array-like field doesn't include at lease one of
        these items.

        Example::

            {"tag": ["a", "b", "c"]} doesn't include "d" from ["c", "d"]
        """
        return {"$not": {"$all": items}}

    @staticmethod
    def item_in(items):
        """
        Single item is in item sets.

        Example::

            {"item_type": "Fruit"}, "Fruit" in ["Fruit", "Meat"]
        """
        return {"$in": items}

    @staticmethod
    def item_not_in(items):
        """
        Single item is not in item sets.

        Example::

            {"item_type": "Seafood"}, "Fruit" not in ["Fruit", "Meat"]
        """
        return {"$nin": items}

    @staticmethod
    def size(n):
        """
        Test if size of an array-like field is n.

        Example::

            filters = {"cart.items": Array.size(3)}
        """
        return {"$size": n}


class Geo2DSphere(object):
    """Geosphere query builder.
    """
    @staticmethod
    def near(lat, lng, max_dist=None, unit_miles=False):
        """Find document near a point.

        For example:: find all document with in 25 miles radius from 32.0, -73.0.
        """
        filters = {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat],
                }
            }
        }
        if max_dist:
            if unit_miles:  # pragma: no cover
                max_dist = max_dist / 1609.344
            filters["$nearSphere"]["$maxDistance"] = max_dist
        return filters


def exists(true_or_false):
    """Test if a field exists.
    """
    return {"$exists": true_or_false}


is_exists = {"$exists": True}
"""Match a field exists.
"""

is_not_exists = {"$exists": False}
"""Match a field not exists.
"""


def mod(divisor, remainder):
    """Test mod(<divisor>) is <remainder>.
    """
    return {"$mod": [divisor, remainder]}


class TypeCode(object):
    """MongoDB Bson type code.
    """
    Double = 1
    String = 2
    Object = 3
    Array = 4
    Binary_Data = 5
    Undefined = 6  # Deprecated
    ObjectId = 7
    Boolean = 8
    Date = 9
    Null = 10
    Regular_Expression = 11
    DBPointer = 12  # Deprecated
    JavaScript = 13
    Symbol = 14  # Deprecated
    JavaScript_with_Scope = 15
    Integer32 = 16
    TimeStamp = 17
    Integer64 = 18
    Decimal128 = 19
    MinKey = -1
    MaxKey = 127
    Number = "number"


def type_is(type_code):
    """Test field type is certain type.
    """
    return {"$type": type_code}


class PipeLine(object):
    @staticmethod
    def random_sample(filters=None, n=5):
        pipeline = list()
        if filters is not None:
            pipeline.append({"$match": filters})
        pipeline.append({"$sample": {"size": n}})
        return pipeline
