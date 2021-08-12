#! /usr/bin/python3
# -*-coding:utf-8-*-
# by lgh
# select interrupting channels

import os
import pymysql
import openpyxl
import requests
import json
import time
import traceback
import sqlite3


# cms
class Cms:
    def __init__(self, ip):
        self.session = None
        self.ip = ip
        # self.tvs = None

    def cms_login(self):
        url = 'http://%s:8180/cms/login.action' % self.ip
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
            # print(name, password)
        except FileNotFoundError:
            print('当前目录下未找到文件：login.txt')

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


def get_server():
    path = os.getcwd() + '/servers.txt'
    server_dict = {}
    try:
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                if line == '\n':
                    pass
                else:
                    line_list = line.split(',')
                    # server_dict[line_list[0].strip()] = line_list[1].strip()
                    server_dict[line_list[1].strip()] = line_list[0].strip()
            # print(server_dict)
    except FileNotFoundError:
        print('当前目录下未找到文件：login.txt')

    return server_dict


def get_list(dict_list):
    if dict_list:
        list_id = []
        list_cp = []
        rows_list = dict_list['rows']
        for i in rows_list:
            list_id.append(i['id'])
            list_cp.append(i['cpcontentid'])
        return list_cp, list_id
    else:
        return [], []


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


if __name__ == '__main__':
    servers_dict = get_server()
    cp_list = servers_dict.keys()
    recovery_all = []
    always_all = []
    add_all = []
    b = MyDb()
    b.connect_db()
    for cp in cp_list:
        try:
            a = Cms(servers_dict[cp])
            a.cms_login()
            # 第一次查询结果
            print("第一次查询开始")
            # 获得当前中断的节目
            # first_list, id_list = get_list(a.select_ch(servers_dict[server]))
            first_list, id_list = get_list(a.select_ch(cp))
            if first_list:
                pass
            else:
                continue
            # print('当前中断的节目：')
            # print(first_list)
            # 下发节目,每台服务器上节目id不一样
            # 判断是否有下发失败的节目
            fail_pu = []
            result_pu = a.publish(id_list).split(',')
            # print(result_pu)
            for m in first_list:
                if m in result_pu:
                    pass
                else:
                    fail_pu.append(m)
            if fail_pu:
                print('下发失败的节目有：')
                print(fail_pu)
            else:
                print('当前中断节目全部下发成功')
            # 同步
            a.syn()
            time.sleep(10)
            a.syn()
            # 第二次查询结果
            # 获得下发同步后中断的节目
            print("第二次查询开始")
            # second_list, id_list2 = get_list(a.select_ch(servers_dict[server]))
            second_list, id_list2 = get_list(a.select_ch(cp))
            # print('下发，同步后中断的节目：')
            # print(second_list)
            # 将中断的节目取消下发
            # print('取消下发成功的节目')
            fail_cal_pu = []
            result_cal_pu = a.cancel_publish(id_list2).split(',')
            for m in second_list:
                if m in result_cal_pu:
                    pass
                else:
                    fail_cal_pu.append(m)
            if fail_cal_pu:
                print('取消下发失败的节目有：')
                print(fail_cal_pu)
            else:
                print('同步后中断节目取消下发成功')
            # 接下来进行数据处理
            first = set(first_list)
            second = set(second_list)
            # 恢复的
            recovery_list = list(first-second)
            print("恢复的节目:")
            print(recovery_list)
            # recovery_all.extend(recovery_list)
            # 一直中断的
            always_list = list(first & second)
            # always_all.extend(always_list)
            # 新增中断
            new_add = list(second-first)
            # add_all.extend(new_add)
            print("新增中断:")
            print(new_add)
            print("一直处于中断状态：")
            print(always_list)
            print('-------------------------------------')


        except Exception as e:

            print('##################################################')
            print('repr(e):\t', repr(e))
            print('traceback.print_exc():\t', traceback.print_exc())
            print('traceback.format_exc():\n', traceback.format_exc())
            print('##################################################')
            continue

    b.close_db()