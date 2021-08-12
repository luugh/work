# -*- coding:UTF-8 -*-
# /usr/bin/python3

# 模拟登录zabbix

import requests
import sys, io
import urllib.parse
import urllib.request
import time
import json
import pymysql

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

r = requests.get('http://119.146.223.77:8000/zabbix/index.php')
# print(r.headers['Set-Cookie'])
phpsessionid = str(r.headers['Set-cookie']).split(';')[0]
print(phpsessionid)
cookie = phpsessionid
print(cookie)

url = 'http://119.146.223.77:8000/zabbix/index.php'


headers = {
    # 'Host': '119.146.223.77:8000',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) ' \
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Accep': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    'Accept-Encoding': "gzip, deflate",
    # 'Origin': 'http://119.146.223.77:8000',
    # 'Referer': "http://119.146.223.77:8000/zabbix/index.php",
    'Content-Type': "application/x-www-form-urlencoded",
    'Content-Length': '89',
    # 'Cookie': cookie,
    'Connection': "keep-alive",
    'Upgrade-Insecure-Requests': '1'
           }

#   login
post_login = urllib.parse.urlencode({

    'form_refresh': '1',
    'name': 'test123',
    'password': '123456',
    'autologin': '1',
    # 'enter': 'Sign+in'
    'enter': 'Sign in'
}).encode("utf-8")
print(post_login)
'''
#get
postdata = urllib.parse.urlencode({
             'broadcasttype': '-1',
             'ids': '',
             'page': '1',
             'qtype': '',
             'query': '',
             'releaseStatus': '2',
             'rp': '100',
             'servicbean.queryWords': '',
             'servicbean.status': '-1',
             'servicbean.type': '-1',
             'sortname':	'channelnumber',
             'sortorder': 'desc',
             'status': '0'
}).encode("utf-8")
'''
url1 = 'http://119.146.223.77:8000/zabbix/index.php?' + post_login.decode()  # 转换成str
# 登录使cookie生效
# req0 = urllib.request.Request(url=url, data=post_login, headers=headers)
# print(req0.data)
# res0 = urllib.request.urlopen(req0)
# print(res0.status)
# res = requests.post(url=url1, headers=headers)
res = requests.post(url=url1, data=post_login, headers=headers)
# req = urllib.request.Request(url=url, data=postdata, headers=headers)
# req = requests.post(url=url, data=postdata, headers=headers)
# print(req.text)
# res = urllib.request.urlopen(req)
# print(res.read().decode('utf-8'))
ex = res
print(res.status_code)
print('文本内容')
print(res.text)
print('响应头')
print(res.headers)
print('获取响应头里的内容')
print(res.headers['Date'])

# ex_list = json.load(ex)
# print(ex_list)
# print(ex_list['rows'][0]['id'])