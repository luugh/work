#! /usr/bin/python3
# -*-coding:utf-8-*-
# by lgh
# @Time     :2019/3/23 17:31
# @Author   :LGH
# @Site     :
# @File     :interrupt_q.py
# @Software :

#! /usr/bin/python3
# -*-coding:utf-8-*-
# by lgh
# select interrupting channels

import os
import pymysql

import requests
import json
import time
import traceback
import sqlite3
import sys


class CmsList:
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
                ch_dict[ch] = '未上架'
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


# cms
class CmsCdn:
    def __init__(self, ip):
        self.session = None
        self.ip = ip
        # self.tvs = None

    def cms_login(self):
        url = 'http://%s:8180/cms/login.action' % self.ip
        name = 'admin'
        password = '5dDrxumL'
        data = {
            'request_locale': 'en_US',
            'userName': name,
            'userPassword': password,
            'checkbox': ''
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Referer': 'http://www.haishilist.com:8180/cms/login.action',
            'Connection': 'keep-alive'
        }
        self.session = requests.Session()
        res = self.session.post(url=url, headers=headers, data=data)
        # print(res.text)
        # print(self.session.cookies)

    def select_ch(self, cp_code):
        print('开始查询 %s 上 %s 的中断信息' % (self.ip, cp_code))
        # self.tv = cp_code
        time.sleep(1)
        headers = {
            'Host': '%s:8081' % self.ip,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://%s:8180/cms//servermonitor/channelrecordlist.action' % self.ip,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            # 'Content-Length': '113',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        select_post = {
            'page': '1',
            'rp': '100',
            'sortname': 'id',
            'sortorder': 'desc',
            'query': '',
            'qtype': '',
            'name': cp_code,
            'status': '',
            'activeStatus': '',
            'streamStatus': '1',    # 1表示中断，2表示正常
            'OnDemandFlag': '',
        }

        select_url = 'http://%s:8180/cms//servermonitor/getChannelRecords.action' % self.ip
        res = self.session.post(url=select_url, data=select_post, headers=headers)
        # 当未查询到中断节目时res.text为''
        if res.text is '':
            print("未查询到中断节目")
            return {}
        else:

            res_j = json.loads(res.text)
            # print(res_j)
            resp_dict = res_j
            return resp_dict

    def publish(self, ids):

        url = 'http://%s:8180/cms//servermonitor/jihuoChannelRecords.action' % self.ip
        headers = {
            'Host': '%s:8081' % self.ip,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Accept': '*/*',
            'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://%s:8180/cms//servermonitor/channelrecordlist.action' % self.ip,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        post_data = {
            'ids': ids
        }
        res = self.session.post(headers=headers, data=post_data, url=url)
        # print(type(res.text))

        return res.text

    def cancel_publish(self, ids):

        url = 'http://%s:8180/cms//servermonitor/stopChannelRecords.action' % self.ip
        headers = {
            'Host': '%s:8081' % self.ip,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Accept': '*/*',
            'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://%s:8180/cms//servermonitor/channelrecordlist.action' % self.ip,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        post_data = {
            'ids': ids
        }
        res = self.session.post(headers=headers, data=post_data, url=url)
        # print(type(res.text))
        if res.text is '':
            print('%s 上中断节目取消下发失败' % self.ip)

        return res.text

    def syn(self):
        url = 'http://%s:8180/cms//servermonitor/refChannelRecord.action' % self.ip

        headers = {
            'Host': self.ip,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Accept': '*/*',
            'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://%s:8180/cms//servermonitor/channelrecordlist.action' % self.ip,
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        res = self.session.get(url=url, headers=headers)
        # print(res.text)
        if res.text == '0':
            print('同步成功')


def get_list(dict_list):
    if len(dict_list) != 0:
        list_cp = []
        dict_name = {}
        cp_stream = {}
        cp_cdn_s = {}
        rows_list = dict_list['rows']
        for i in rows_list:
            list_cp.append(i['cpcontentid'])
            dict_name[i['cpcontentid']] = i['remark']
            cp_stream[i['cpcontentid']] = i['streamStatus']
            cp_cdn_s[i['cpcontentid']] = i['statusStr']

        return list_cp, dict_name, cp_stream, cp_cdn_s
    else:
        return [], {}, {}, {}


class MyDb:
        def __init__(self):
            self.name = 'channelaction'
            self.pass_wd = 'd0177951d1493f49'
            self.db_name = 'cmdb'
            self.port = '3306'
            self.host = '208.81.204.10'

        def connect_db(self):
            db_connect = pymysql.connect(self.host, self.name, self.pass_wd, self.db_name)
            return db_connect

        def get_data(self, command):
            cursor = self.connect_db().cursor()
            select_command = command
            cursor.execute(select_command)
            results = cursor.fetchall()

            return results

        def close_db(self):
            self.connect_db().close()


class MySqlite:

    def __init__(self, name):
        self.db_name = name
        self.name = name

    def create_db(self):
        dir_list = os.listdir('.')
        check = 0
        for file_name in dir_list:
            if self.name in file_name:
                check = 1

        if check == 0:
            path = os.getcwd() + '/' + self.name
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            create_table = 'create table interrupt(id integer primary key not null , cp_code char(20),' \
                           'ch_id char(20), ip char(20))'
            cursor.execute(create_table)
            cursor.close()
            cursor.close()
            conn.commit()
            conn.close()

    def connect_db(self):
        connect = sqlite3.connect(self.name)
        return connect

    def excute(self, insert_sql, connect):
        cursor = connect.cursor()
        cursor.execute(insert_sql)
        cursor.close()
        connect.commit()

    def close_connect(self, connect):
        connect.close()


def export_result():
    file_path = os.getcwd() + '/interrupt_data.db'
    a = MySqlite(file_path)
    conn_q = a.connect_db()
    sql_cpmmand = 'select * from TV_server'


    # # servers_dict = get_server()
    # # cp_list1 = servers_dict.keys()
    # list_cp_all = []
    # cp_name = {}
    # cp_stream_all = {}
    # cp_cdn_s_all = {}
    # cp_list_s_all = {}
    # cp_cdn = {}
    #
    # for cp in cp_list1:
    #     try:
    #         cp_cdn1 = {}
    #         a = CmsCdn(servers_dict[cp])
    #         a.cms_login()
    #         # 第一次查询结果
    #         print("第一次查询开始")
    #         # 获得当前中断的节目
    #         a.syn()
    #         # first_list, id_list = get_list(a.select_ch(servers_dict[server]))
    #         list_cp, dict_name, cp_stream, cp_cdn_s = get_list(a.select_ch(cp))
    #         if len(list_cp) == 0:
    #             pass
    #         else:
    #             list_cp_all = list_cp_all + list_cp
    #             cp_name.update(dict_name)
    #             cp_stream_all.update(cp_stream)
    #             cp_cdn_s_all.update(cp_cdn_s)
    #         for cpc in list_cp:
    #             cp_cdn1[cpc] = servers_dict[cp]
    #         cp_cdn.update(cp_cdn1)
    #     except Exception as e:
    #         print('##################################################')
    #         print('repr(e):\t', repr(e))
    #         print('traceback.print_exc():\t', traceback.print_exc())
    #         print('traceback.format_exc():\n', traceback.format_exc())
    #         print('##################################################')
    #         continue
    # b = CmsList()
    # b.cms_login()
    # cp_list_s_all = b.select_ch(list_cp_all)
    #
    # return list_cp_all, cp_name, cp_stream_all, cp_cdn_s_all, cp_list_s_all, cp_cdn


if __name__ == '__main__':
    export_result()
    # list_cp_all, cp_name, cp_stream_all, cp_cdn_s_all, cp_list_s_all, cp_cdn = export_result()
    # # print(list_cp_all)
    # # print(cp_name)
    # # print(cp_stream_all)
    # # print(cp_list_s_all)
    # # print(cp_cdn_s_all)
    # # print(cp_cdn)
    # file = open('/root/django/thirdpart/watch/interrupt_q/log.txt', 'w')
    # file.write(str(list_cp_all));
    # file.close()
