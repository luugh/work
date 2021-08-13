# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2021/1/29 10:52
# @Author  : LGH
# @File    : SE.py
# @Software: PyCharm
import json
import os
import time
import requests
import asyncio
import yaml

class Cms:
    def __init__(self, ip):
        self.ip = ip
        self.session = ''

    # get session
    async def login(self):
        ip = self.ip
        url = 'http://%s:8088/user/login' % ip
        host = '%s:8088' % ip
        referer = 'http://%s:8088/user/login' % ip
        # headers = {
        #     # 'Host': 'xxx.xxx.6.62:8088',
        #     'Host': host,
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        #                   'Chrome/78.0.3904.108 Safari/537.36',
        #     'Accept': "application/json",
        #     'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
        #     'Accept-Encoding': 'gzip, deflate',
        #     'Content-Type': 'application/json; charset=utf-8',
        #     'Referer': referer,
        #     'Connection': 'keep - alive',
        #     # 'DNT': '1',
        #     'origin': 'http://%s:8088' % ip,
        #     # 'Cookie': self.cookie
        # }
        login_url = 'http://%s:8088/cdn/submitLogin' % ip
        with open("./conf.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        # name = 'admin'
        # passwd = 
        login_post = {

            "userName": cfg["SE"]["login_name"],
            "password": cfg["SE"]["password"],
            "type": "account",
            "local": "en_US",
        }
        # print(login_post)
        self.session =requests.Session()
        # 注意此时用的json参数
        res = self.session.post(url=login_url, json=login_post)

        # SHIROSESSION = 97229d9a-912b-4a19-a685-9cef7a3fddd4;Path = /;
        # print(res.headers['Set-Cookie'])
        # cookie = res.headers['Set-Cookie']
        # cookie = 'SHIROSESSION=97229d9a-912b-4a19-a685-9cef7a3fddd4;Path = /'
        # 正向后视断定
        # test = re.findall(r'(?<=SHIROSESSION=)[^;]+', cookie)

        # print(test)
        # print(self.cookie)
        # print(res.status_code)
        # print(res.text)
        # print(res.headers)
        # print(res.headers['date'])

    def sync_ch(self, time1):
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
        # }
        url = 'http://{}:8088/cdn/record/sync'.format(self.ip)
        self.session.get(url)
        time.sleep(time1)

    # get channels status in batch
    def select_batch(self, ip, state, origin, pagesize):
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
        # }
        url = 'http://{}:8088/cdn/record?seconds=300&state={}&origin={}&current=1&pageSize={}'.format(ip, state, origin, pagesize)
        res = self.session.get(url=url)
        print(f'seletc: {res.text}')
        return res.text

    async def select_ch(self, cpcode):

        select_url = 'http://{}:8088/cdn/record?channel_id={}&pageSize=1000'.format(self.ip, cpcode)
        # res = requests.post(url=select_url, data=select_post, headers=headers)
        # res = requests.get(url=select_url, headers=headers)
        res = self.session.get(url=select_url)
        # print(res.text)
        # print(type(res.text))
               
        # res.text输出内容为字符串，需要转换为字典
        res_dict = json.loads(res.text)
        if res_dict['pagination']['total'] != 0:
            for ch in res_dict['list']:
                if ch['channel_id'] == cpcode:
                    return ch
        else:
            return res.text

    async def modify_ch(self, kwargs):

        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        url = 'http://{}:8088/cdn/record'.format(self.ip)
        data = {
            "channel_id": kwargs['channel_id'],
            "channel_name": kwargs['channel_name'],
            "id": kwargs['id'],
            "issue_state": kwargs['issue_state'],
            "on_demand": kwargs['on_demand'],
            "origin": kwargs['origin'],
            "select_app": kwargs['select_app'],
            "source_url": kwargs['source_url'],
            "store_time": kwargs['store_time']
        }
        data_str = json.dumps(data)

        res = self.session.post(url=url, data=data_str, headers=headers)
        res_dict = json.loads(res.text)
        # print(type(res_dict))
        # print(res.headers)
        # if res_dict['code'] == 200:
        #     print('change success!')
        #     return
        # else:
        #     print(res_dict)
        return res.text