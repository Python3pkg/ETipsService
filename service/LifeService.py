#!/usr/bin/python
#coding=utf-8
__author__ = 'Jayin Ton'
import requests
from bs4 import BeautifulSoup
import _
"""
knowning problems:
1.他服务器有防御型，不能频繁请求，不然不行
"""


apart = {
    "34": "1",
    "35": "9",
    "36": "17",
    "37": "25",
    "1": "33",
    "2": "40",
    "3": "47",
    "4": "55",
    "5": "63",
    "6": "68",
    "19": "74",
    "20": "75",
    "21": "76",
    "22": "77",
    "14": "105",
    "15": "114",
    "38": "122",
    "39": "123",
    "40": "124",
    "41": "214",
    "42": "226",
    "43": "227"
}


def _get_electricity_info_html(apart_id, meter_room):
    """"
     apartID:栋数
     meterRoom:宿舍号
    """
    if apart.get(apart_id) is None:
        pass  #error input
    post_data = {
        "action": "search",
        "apartID": apart.get(apart_id),
        "meter_room": apart_id + meter_room
    }
    r = requests.post("http://202.192.252.140/index.asp", data=post_data)
    return r.content.decode(_.get_charset(r.content))


def _get_tag_span(tag):
    if tag.has_attr('class'):
        pass


def get_electricity_info(apart_id, meter_room):
    apart_id = str(apart_id)
    meter_room = str(meter_room)
    content = _get_electricity_info_html(apart_id, meter_room)
    soup = BeautifulSoup(content)
    tags = soup.find_all(name='span', class_='STYLE7')
    result = {
        'apart': _.trim(tags[0].string),
        'apart_id':  _.trim(tags[1].string),
        'used':  _.trim(tags[2].string),
        'left':  _.trim(tags[3].string),
        'update_time':  _.trim(tags[4].string)
    }
    return _.to_json_string(result)

if __name__ == '__main__':
    print get_electricity_info(3, 706)
