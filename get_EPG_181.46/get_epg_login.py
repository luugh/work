# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2020/9/29 9:16
# @Author  : LGH
# @File    : get_epg.py
# @Software: PyCharm

import requests
import openpyxl
import os
import json
import time


class LoginEpg:
    def __init__(self):
        self.session = None

    def epg_login(self):
        url = 'http://34.245.181.46:8456/submitLogin'
        path = os.getcwd() + r'\login.txt'
        line_list = []
        try:
            with open(path) as f:
                lines = f.readlines()
                for line in lines:
                    if line == '\n':
                        pass
                    else:
                        line_list.append(line)
            # print(line_list)
            name = line_list[0].strip()
            password = line_list[1].strip().replace("'", "")
            print(name, password)
        except Exception as err:
            print(err)
            print('当前目录下未找到文件：login.txt')

        data = {

            'userName': name,
            'password': password,

        }
        headers = {
            'Host': '34.245.181.46:8456',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '40',
            'Origin': 'http://34.245.181.46:8456',
            'Connection': 'keep-alive',
            'Referer': 'http://34.245.181.46:8456/logout',
        }
        self.session = requests.Session()
        res = self.session.post(url=url, headers=headers, data=json.dumps(data))
        print(res.content)
        print(res.status_code)
        print(self.session.cookies.items())
        print(res.headers)

    def select_spider(self):
        # url = 'http://34.245.181.46:8456/spider'
        url = 'http://34.245.181.46:8456/check/getSpiderTable?page=1&limit=10'
        cookie = self.session.cookies.items()[0][1]
        print(cookie)
        headers = {
            'Host': '34.245.181.46:8456',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'http://34.245.181.46:8456/LoginOut',
            # 'Cookie': cookie,
            'Upgrade-Insecure-Requests': '1',
        }
        # res = requests.get(url=url,headers=headers)
        res = self.session.get(url, headers=headers)
        print(res.status_code)
        print(res.text)


if __name__ == '__main__':
    a = LoginEpg()
    a.epg_login()
    a.select_spider()