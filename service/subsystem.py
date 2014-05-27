#!/usr/bin/env python
#coding=utf-8
__author__ = 'Jayin Ton'

import _
import copy
import requests
from bs4 import BeautifulSoup

_headers = None


class subSystem(object):
    def __init__(self, userid, userpsw):
        self._headers = None
        self._userid = userid
        self._userpsw = userpsw

    def _get_rndnum_cookies(self):
        """
        get the randomNumber
        """
        r = requests.get("http://jwc.wyu.edu.cn/student/rndnum.asp")
        # print r.cookies['ASPSESSIONIDSCRRDTBQ']
        # print r.cookies['LogonNumber']
        return r.cookies

    def login(self):
        cookies = self._get_rndnum_cookies()
        UserCode, UserPwd = self._userid, self._userpsw
        Validate = cookies['LogonNumber']
        Submit = "%CC%E1+%BD%BB"
        headers = {'Referer': 'http://jwc.wyu.edu.cn/student/body.htm',
                   "Cookie": 'ASPSESSIONIDSCRRDTBQ' + "=" + cookies['ASPSESSIONIDSCRRDTBQ'] + ";LogonNumber=" +
                             cookies[
                                 'LogonNumber']}
        #save header
        self._headers = headers
        data = {
            "UserCode": UserCode,
            "UserPwd": UserPwd,
            "Validate": Validate,
            "Submit": Submit,

        }
        r = requests.post("http://jwc.wyu.edu.cn/student/logon.asp", data=data, headers=headers)
        # print r.content.decode(_.get_charset(r.content))
        return True if r.status_code == 200 else False

    def _get_course_html(self):
        r = requests.get("http://jwc.wyu.edu.cn/student/f3.asp", headers=self._headers)
        print r.content.decode(_.get_charset(r.content))


    def _get_score_html(self):
        self._headers['Referer'] = "http://jwc.wyu.edu.cn/student/menu.asp"
        r = requests.get("http://jwc.wyu.edu.cn/student/f4_myscore11.asp", headers=self._headers, allow_redirects=False)
        print r.content.decode(_.get_charset(r.content))


if __name__ == '__main__':
    u = subSystem("3112002722", '931127')
    print u.login()
    if u.login():
        # u._get_course_html()
        u._get_score_html()