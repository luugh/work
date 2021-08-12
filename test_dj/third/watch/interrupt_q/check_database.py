#! /usr/bin/python3
# -*-coding:utf-8-*-
# by lgh
# @Time     :2019/3/23 15:54
# @Author   :LGH
# @Site     :
# @File     :check_database.py
# @Software :
import os
import sqlite3


def check_data():
    dir_list = os.listdir('./')
    file_path = os.getcwd()
    # print(dir_list)
    # print(file_path)
    check = 0
    for file_name in dir_list:
        if 'interrupt_data.db' in file_name:
            check = 1
    # print(check)
    if check == 0:
        conn = sqlite3.connect(file_path + '/interrupt_data.db')
        cursor = conn.cursor()
        create_target = 'create table TV_server(id integer primary key not null,cp_code char (20),' \
                        'server_ip char (20))'
        create_data = 'create table data_tables(id integer primary key not null,cpc char (20),ch_name char (20),' \
                      'stream_sta char (20),cdn_sta char (20),list_sta char (20),server_sor char (20),' \
                      'select_time char (20))'
        cursor.execute(create_target)
        cursor.execute(create_data)
        cursor.close()
        conn.commit()
        conn.close()


if __name__ == '__main__':
    check_data()
