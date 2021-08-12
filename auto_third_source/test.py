# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2021/1/29 10:44
# @Author  : LGH
# @File    : test.py
# @Software: PyCharm


from SE_Operation import SE
import json

if __name__ == '__main__':
    ip = '38.94.97.150'
    a = SE.Cms(ip)
    a.login()
    res = a.select_ch('TV77259')
    print(res)
    res_dict = json.loads(res)
    ch_dict = res_dict['list'][0]
    print('ch_dict:{}'.format(ch_dict))
    ch_dict['origin'] = '青蛙146_EN'
    a.modify_ch(ch_dict)
