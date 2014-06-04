# !/usr/bin/env python
# coding=utf-8
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
        # save header
        self._headers = headers
        data = {
            "UserCode": UserCode,
            "UserPwd": UserPwd,
            "Validate": Validate,
            "Submit": Submit,

        }
        r = requests.post("http://jwc.wyu.edu.cn/student/logon.asp", data=data, headers=headers, cookies=self._cookies)
        # print r.content.decode(_.get_charset(r.content))
        return True if r.status_code == 200 else False

    def _get_course_html(self):
        self._headers['Referer'] = "http://jwc.wyu.edu.cn/student/menu.asp"
        r = requests.get("http://jwc.wyu.edu.cn/student/f3.asp", headers=self._headers, cookies=self._cookies)
        return r.content.decode(_.get_charset(r.content))

    def get_course(self):
        html = self._get_course_html()
        soup = BeautifulSoup(markup=html)
        # tbodys[0]为学生信息，tbodys[1]课表，tbodys[2]为课程详情
        tbodys = soup.find_all(name='tbody')
        result = {
            'course': []
        }
        for x in tbodys[1].select('td[valign=top]'):
            # print x.getText(separator=u" ")
            texts = x.getText(separator=u" ").split(u" ")
            # have no lesson
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

    # 获取每列信息，除去首行（课程代号..）
    def get_td(self, tag):
        if tag.name == "td" and not "background" in tag.get("style"):
            return True
        return False

    def get_score(self):
        html = self._get_score_html()
        soup = BeautifulSoup(html)
        div = soup.find_all("div", class_="Section1")[0]
        tag_ps = div.find_all("p")
        del tag_ps[0]
        result = {
            "response": []
        }
        """
        #one object
        {
           "year":"第一学期",
           "score_list":[
                {
                    "id":"0800040",
                    "name":"C++"
                    "type":"必修",
                    "xuefen":"1",
                    "score":"95",
                    "remark":"重修"
                }
           ]
        }
        """
        # 最后一个为第二课堂学分,删除之
        tables = soup.find_all("table", attrs={"class": "MsoTableGrid", "border": "1"})
        del tables[len(tables) - 1]
        # 第x个学期
        year_num = 1
        for table in tables:
            try:
                trs = table.find_all("tr")

                tern_info = {
                    "year": year_num,
                    "score_list": []
                }

                # 遍历每一列
                for tr in trs:
                    tds = tr.find_all(self.get_td)
                    if len(tds) == 0:
                        continue
                    lesson_info = {

                        "id": _.trim(tds[0].get_text()),
                        "name": _.trim(tds[1].get_text()),
                        "type": _.trim(tds[2].get_text()),
                        "xuefen": _.trim(tds[3].get_text()),
                        "score": _.trim(tds[4].get_text()),
                        "remark": _.trim(tds[5].get_text())
                    }

                    tern_info["score_list"].append(lesson_info)
                year_num += 1
                result["response"].append(tern_info)
            except Exception as e:
                _.d(e.message)
        # print result
        return result

    def _get_stu_info(self):
        r = requests.get("http://jwc.wyu.edu.cn/student/f1.asp", headers=self._headers, cookies=self._cookies)
        print r.content.decode(_.get_charset(r.content))


if __name__ == '__main__':
    u = SubSystem("3112002722", '931127')
    # print u.login()
    if u.login():
        print "****************Login success!**************"
        print "****************course list**************"
        # print u.get_course()
        print u.get_score()
        # u._get_stu_info()