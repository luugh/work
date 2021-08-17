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


class Cms:
    def __init__(self, ip):
        self.ip = ip
        self.session = ''

    # get session
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

        # SHIROSESSION = 97229d9a-912b-4a19-a685-9cef7a3fddd4;Path = /;
        # print(res.headers['Set-Cookie'])
        cookie = res.headers['Set-Cookie']
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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
        }
        url = 'http://{}:8088/cdn/record/sync'.format(self.ip)
        self.session.get(url)
        time.sleep(time1)

    # get channels status in batch
    def select_batch(self, ip, state, origin, pagesize):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
        }
        url = 'http://{}:8088/cdn/record?seconds=300&state={}&origin={}&current=1&pageSize={}'.format(ip, state, origin, pagesize)
        res = self.session.get(url=url, headers=headers)
        print(res.text)
        return res.text

    def select_ch(self, cpcode):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Connection': 'keep-alive',
        }

        # select_post = {
        #     'pageSize': '100',
        #     'channel_id': cpcode,
        # }

        select_url = 'http://{}:8088/cdn/record?channel_id={}&pageSize=1000'.format(self.ip, cpcode)
        # res = requests.post(url=select_url, data=select_post, headers=headers)
        # res = requests.get(url=select_url, headers=headers)
        res = self.session.get(url=select_url, headers=headers)
        # print(res.text)
        # print(type(res.text))
        # res.text输出内容为字符串，需要转换为字典
        return res.text

    def modify_ch(self, kwargs):
        # {
        #     "channel_id": "TV77259",
        #     "channel_name": "TSN 5-EN",
        #     "id": 1144543,
        #     "issue_state": 106,
        #     "on_demand": "0",
        #     "origin": "青蛙146_EN",
        #     "select_app": "20",
        #     "source_url": "http://xxxxx:8082/TVxxxx",
        #     "store_time": "0"
        # }
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
        print('modify_data:{}'.format(data))
        res = self.session.post(url=url, data=data_str, headers=headers)
        res_dict = json.loads(res.text)
        print(res_dict)
        # print(res.headers)
        # if res_dict['code'] == 200:
        #     print('change success!')
        #     return
        # else:
        #     print(res_dict)
        return res.text

    def issue(self, id):
        url = 'http://{}:8088/cdn/channel/issue'.format(self.ip)
        data = {
            "channel_id_list": [id]
        }
        # print(data)
        res = self.session.post(url=url, json=data)
        res_dict = json.loads(res.text)
        if res_dict['code'] == 200:
            print('下发成功！')
        else:
            print(res.text)

    def up_tr_file(self, file_path):
        url = "http://{}:8088/cdn/channel/import".format(self.ip)
        cover_url = "http://{}:8088/cdn/importChannelCover".format(self.ip)
        cover_data = {
            "cover": "cover"
        }

        file = {
            # "Content-Disposition": "form-data",
            # "name": "file",
            # "filename": "TV3145Transcode-20210314234159.xlsx",
            # "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            'file': (file_path,
                     open(file_path, 'rb'),
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        }

        res = self.session.post(url=url, files=file)
        res_dict = json.loads(res.text)
        if res_dict['code'] == 201:
            print('上传成功！')
        else:
            print(res.text)

        res1 = self.session.post(url=cover_url, json=cover_data)
        res1_dict = json.loads(res1.text)
        if res1_dict['code'] == 201:
            print('覆盖成功！')
        else:
            print(res1.text)

    def select_tr_ch(self, cpcode):
        url = 'http://{}:8088/cdn/channel?channel_id={}&seconds=60&current=1&pageSize=10'.format(self.ip, cpcode)
        res = self.session.get(url)

        return res.text