#!/usr/bin/python3
# -*- coding:utf-8 -*-
# by lgh
#

import requests
import openpyxl
import os
import json
import time


class Cms:
    def __init__(self):
        self.session = None

    def cms_login(self):
        url = 'http://www.haishilist.com:8180/cms/login.action'

        data = {
            'request_locale': 'en_US',
            'userName': '刘冠华',
            'userPassword': '7Wg4ne6T8f',
            'checkbox': ''
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Referer': 'http://www.haishilist.com:8180/cms/login.action',
            'Connection': 'keep-alive'
        }
        self.session = requests.Session()
        res = self.session.post(url=url, headers=headers, data=data)
        # print(res.status_code)

    def select_ch(self, ch_list):
        ch_dict = {}
        url = 'http://www.haishilist.com:8180/cms//channel/channelList.action?hasInput=N'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Referer': 'http://www.haishilist.com:8180/cms/login.action',
            'Connection': 'keep-alive'
        }
        for ch in ch_list:
            time.sleep(1)
            data = {
                'page': '1',
                'rp': '15',
                'sortname': 'channelnumber',
                'sortorder': 'desc',
                'query': '',
                'qtype': '',
                'servicbean.queryWords': ch,
                # 'servicbean.queryWords': 'TV77051',
                'servicbean.type': '-1',
                'servicbean.status': '-1',
                'status': '0',
                'releaseStatus': '0',
                'broadcasttype': '-1',
                'ids': ''
            }
            res = self.session.post(url=url, headers=headers, data=data)
            # print(res.text)
            # print(res.status_code)
            res_dict = json.loads(res.text)
            # print(res_dict)
            # print(type(res_dict['rows']))
            if len(res_dict['rows']) == 0:
                print('%s 不存在于列表中' % ch)
                ch_dict[ch] = '不在列表中'
            else:
                # print('%s 在列表中' % ch)
                keywords = self.judge_status(res_dict)
                print(ch, keywords)
                ch_dict[ch] = keywords

        return ch_dict

    @classmethod
    def judge_status(cls, res_dict):
        num = res_dict['total']
        # print(num)
        rows_list = res_dict['rows']
        status = rows_list[0]['releaseStatus']
        values = '0'
        if num == 1:
            values = '1'
        else:
            for i in range(1, num):
                if status == rows_list[i]['releaseStatus']:
                    values = '1'
                else:
                    values = '2'
                    break
        if values == '1':
            if status == '1':
                keywords = '列表已上线'
            else:
                keywords = '列表已下线'
        else:
            keywords = '列表下发状态不一致'
        return keywords


def cp_lists(list1):
    a = Cms()
    a.cms_login()
    re_dict = a.select_ch(list1)

    return re_dict

