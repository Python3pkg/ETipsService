# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import _


class WyuNews(object):
    def __init__(self):
        pass

    @staticmethod
    def _get_tag_a(tag):
        if tag.has_attr('href') and tag.has_attr('target'):
            if 'http://' in tag.attrs['href']:
                return False
            return True
        return False

    @staticmethod
    def _wyu_news( page):
        url = 'http://www.wyu.cn/news/default.asp'
        params = {'page': page}
        r = requests.get(url, params=params)
        encoding = _.get_charset(r.content)
        return r.content.decode(encoding)


    def get_wyu_news(self, page):
        response = {
            'result': []
        }
        if page <= 0:
            return response
        res = WyuNews._wyu_news(page)
        soup = BeautifulSoup(res, from_encoding='utf-8')
        tag_a = soup.find_all(self._get_tag_a)
        result = []
        for item in tag_a:
            result.append({
                'url': ''.join(('http://www.wyu.cn/news/', item.attrs['href']))
                , 'title': item.string
            })
        response['result'] = result
        return _.to_json_string(response)
