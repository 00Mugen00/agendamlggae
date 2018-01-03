# -*- coding: utf-8 -*-
""" Converts from JSON to Python or from Python to JSON the right way """

import ujson


def from_json(json_str):
    """
    Given a json str/unicode, returns a Python-mapped object of it. Uses dict and lists to achieve it. All strings
    stored inside the structure are unicode.

    :param json_str:
        A str/unicode string with JSON
    :return:
        dict/list object with the JSON parsed inside it
    """
    return ujson.loads(json_str)


def to_json(obj):
    """
    Given a python object (dict, list or any kind of object), converts it to JSON and returns a unicode string.

    :param obj:
        A object to convert
    :return:
        Unicode string with the object converted to JSON
    """
    return ujson.dumps(obj, ensure_ascii=False).decode('utf-8')
