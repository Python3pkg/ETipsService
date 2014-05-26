#!/usr/bin/python
#coding=utf-8
__author__ = 'Jayin Ton'

import re
import json

def get_charset(html):
    """
    get charset in html page
    return : default if not exist `charset`
    """
    regex = r'charset=([a-zA-Z0-9-]+)?'
    pattern = re.compile(regex, re.IGNORECASE)
    if len(pattern.findall(html)) == 0:
        return 'UTF-8'
    return pattern.findall(html)[0]


def to_json_string(obj):
    return json.dumps(obj)


def trim(string):
    return string.strip()

