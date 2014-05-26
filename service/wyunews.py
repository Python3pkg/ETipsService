#!/usr/bin/python
#coding=utf-8
__author__ = 'Jayin Ton'

import requests
import re
from bs4 import BeautifulSoup
import json

regex = r'charset=([a-zA-Z0-9-]+)?'
pattern = re.compile(regex, re.IGNORECASE)


def get_tag_a(tag):
    if tag.has_attr('href') and tag.has_attr('target'):
        if 'http://' in tag.attrs['href']:
            return False
        return True
    return False


def wyu_news(page):
    url = 'http://www.wyu.cn/news/default.asp'
    params = {'page': page}
    r = requests.get(url, params=params)
    encoding = pattern.findall(r.content)[0]
    return r.content.decode(encoding)  #Binary Response Content


def get_wyu_news(page):
    response = {
        'result': []
    }
    if page <= 0:
        return response
    res = wyu_news(page)
    soup = BeautifulSoup(res, from_encoding='utf-8')
    tds = soup.find_all(get_tag_a)
    result = []
    for item in tds:
        result.append({
            'url': ''.join(('http://www.wyu.cn/news/', item.attrs['href']))
            , 'title': item.string
        })
    response['result'] = result
    return json.dumps(response)


# if __name__ == '__main__':
#     print (get_wyu_news(1))
