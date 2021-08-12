#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2021/2/2 20:02
# @Author  : LGH
# @File    : get_living_best.py
# @Software: PyCharm

from SE import Cms
import json
import time

if __name__ == '__main__':
    start = time.time()
    a = Cms('54.78.82.194')
    a.login()
    best_TV = []
    res_text = a.get_all()
    print(res_text)
    res_dic = json.loads(res_text)
    tv_list = res_dic['list']
    address = 'cmc.best-tv.me'
    for tv in tv_list:
        if address in tv['source_url']:
            best_TV.append(tv['channel_id'])
    print(best_TV)
    with open('./bestTV.txt', 'w+') as f:
        for tv in best_TV:
            f.write(tv+'\n')
    end = time.time()
    print('use time:{}'.format(end-start))