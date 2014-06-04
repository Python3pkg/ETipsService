#!/usr/bin/env python
#coding=utf-8
__author__ = 'Jayin Ton'

import _
import copy
import requests
from bs4 import BeautifulSoup

_headers = None


class SubSystem(object):
    def __init__(self, userid, userpsw):
        self._headers = None
        self._cookies = None
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
        self._cookies = self._get_rndnum_cookies()
        # print self._cookies
        UserCode, UserPwd = self._userid, self._userpsw
        Validate = self._cookies['LogonNumber']
        Submit = "%CC%E1+%BD%BB"
        headers = {'Referer': 'http://jwc.wyu.edu.cn/student/body.htm'}
        #save header
        self._headers = headers
        data = {
            "UserCode": UserCode,
            "UserPwd": UserPwd,
            "Validate": Validate,
            "Submit": Submit,

        }
        r = requests.post("http://jwc.wyu.edu.cn/student/logon.asp", data=data, headers=headers, cookies=self._cookies)
        #print r.content.decode(_.get_charset(r.content))
        return True if r.status_code == 200 else False

    def _get_course_html(self):
        self._headers['Referer'] = "http://jwc.wyu.edu.cn/student/menu.asp"
        r = requests.get("http://jwc.wyu.edu.cn/student/f3.asp", headers=self._headers, cookies=self._cookies)
        return r.content.decode(_.get_charset(r.content))

    def get_course(self):
        html = self._get_course_html()
        soup = BeautifulSoup(markup=html)
        #tbodys[0]为学生信息，tbodys[1]课表，tbodys[2]为课程详情
        tbodys = soup.find_all(name='tbody')
        result = {
            'course': []
        }
        for x in tbodys[1].select('td[valign=top]'):
            # print x.getText(separator=u" ")
            texts = x.getText(separator=u" ").split(u" ")
            #have no lesson
            if len(texts) == 1:
                lesson = {
                    'name': u"",
                    'time': u"",
                    'address': u"",
                    'teacher': u""
                }
            else:
                lesson = {
                    'name': texts[0],
                    'time': texts[1],
                    'address': texts[2].split(u" ")[0],
                    'teacher': texts[2].split(u" ")[1]
                }
            # print lesson
            result['course'].append(lesson)

        return _.to_json_string(result)

    def _get_score_html(self):
        self._headers['Referer'] = "http://jwc.wyu.edu.cn/student/menu.asp"
        r = requests.get("http://jwc.wyu.edu.cn/student/f4_myscore11.asp", headers=self._headers, allow_redirects=False,
                         cookies=self._cookies)
        return r.content.decode(_.get_charset(r.content))

    @staticmethod
    def tag_tables(self):
        pass
    def get_score(self):
        html = self._get_score_html()
        soup = BeautifulSoup(html)
        res =soup.find_all()

        print res


    def _get_stu_info(self):
        r = requests.get("http://jwc.wyu.edu.cn/student/f1.asp", headers=self._headers, cookies=self._cookies)
        print r.content.decode(_.get_charset(r.content))


if __name__ == '__main__':
    u = SubSystem("3112002722", '931127')
    print u.login()
    if u.login():
        print "****************Login success!**************"
        print "****************course list**************"
        #print u.get_course()
        print u._get_score_html()
        #u._get_stu_info()