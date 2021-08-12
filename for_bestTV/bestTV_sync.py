# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2021/1/31 9:23
# @Author  : LGH
# @File    : bestTV_channel.py
# @Software: PyCharm


import requests

class SE:

    def __init__(self):
        self.name = 'bestTV_state'
        self.passwd = 'YBMXBj0K'
        self.ip = '54.78.82.194'

    def login(self):
        ip = self.ip
        url = 'http://%s:8088/user/login' % ip
        host = '%s:8088' % ip
        referer = 'http://%s:8088/user/login' % ip
        headers = {
            # 'Host': '178.132.6.62:8088',
            'Host': host,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/78.0.3904.108 Safari/537.36',
            'Accept': "application/json",
            'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json; charset=utf-8',
            'Referer': referer,
            'Connection': 'keep - alive',
            # 'DNT': '1',
            'origin': 'http://%s:8088' % ip,
            # 'Cookie': self.cookie
        }
        login_url = 'http://%s:8088/cdn/submitLogin' % ip
        filepath = os.getcwd() + r'/login.txt'
        with open(filepath, 'r') as f:
            list = f.readlines()
        name = list[0].strip()
        passwd = list[1].strip()
        # name = 'admin'
        # passwd = 'Q5t0wRLN'
        login_post = {

            "userName": name,
            "password": passwd,
            "type": "account",
            "local": "en_US",
        }
        # print(login_post)
        self.session = requests.Session()
        # 注意此时用的json参数
        res = self.session.post(url=login_url, json=login_post, headers=headers)

    def sync_ch(self, time1):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
        }
        url = 'http://{}:8088/cdn/record/sync'.format(self.ip)
        self.session.get(url)
        time.sleep(time1)
