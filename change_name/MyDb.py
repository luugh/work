#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2021/2/6 12:11
# @Author  : LGH
# @File    : MyDb.py
# @Software: PyCharm

from collections import defaultdict
import pymysql


class MyDb:

    def __init__(self):
        self.name = 'channelaction'
        self.passwd = 'd0177951d1493f49'
        self.dbname = 'cmdb'
        self.port = '3306'
        self.host = '38.83.75.10'
        self.db = None

    def connect_db(self):
        self.db = pymysql.connect(host=self.host, user=self.name, password=self.passwd, database=self.dbname)
        return self.db

    def get_info(self, name):
        while True:
            try:
                # print(name)
                cursor = self.db.cursor()
                select_command = u"select hostIp from cdnChannel where channelMark='%s';" % name
                cursor.execute(select_command)
                results = cursor.fetchall()
                # print(type(results))
                name_list = []
                # print('results: {}'.format(results))
                if len(results) != 0:
                    name_list.append(name)
                    server_dict1 = defaultdict(list)
                    for n in results:
                        server_dict1[n[0]].append(name)
                else:
                    select_command1 = 'select hostIp,channelMark from cdnChannel where channelMark like "%' + name + '@%";'
                    # print(select_command1)
                    cursor.execute(select_command1)
                    results = cursor.fetchall()
                    print('results: {}'.format(results))
                    server_dict1 = defaultdict(list)
                    for n in results:
                        if n[1] not in name_list:
                            name_list.append(n[1])
                        server_dict1[n[0]].append(n[1])
                    # print('get-server_dict: {}'.format(server_dict1))
                    # print('name_list: {}'.format(name_list))
                # 返回ip列表
                break
            except pymysql.OperationalError as e:
                print(e)
                self.db.ping()
                self.connect_db()
        # print('name_list: {}'.format(name_list))
        # print('server_dict: {}'.format(server_dict1))
        return name_list, server_dict1

    def close(self, connect_db):
        connect_db.close()