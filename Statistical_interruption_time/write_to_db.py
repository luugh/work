#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2021/3/1 15:32
# @Author  : LGH
# @File    : write_to_db.py
# @Software: PyCharm

import os
import sys
import sqlite3


def db_exist(path):
    conn = sqlite3.connect(path+'/bestTV.db')
    cursor = conn.cursor()
    sql1 = 'CREATE TABLE ch_info' \
           '(id INT  NOT NULL AUTOINCREMENT,' \
           ' cpcode CHAR(10) PRIMARY KEY NOT NULL,' \
           ' name CHAR(20) NOT NULL,' \
           ' link CHAR(100) NOT NULL,' \
           ' origin CHAR(20));'
    sql2 = 'CREATE TABLE c_state_latest' \
           '(id INT NOT NULL AUTOINCREMENT,' \
           ' cpcode CHAR(10) PRIMARY KEY NOT NULL,' \
           ' state INT(1) NOT NULL);'
    sql3 = 'CREATE TABLE ch_event' \
           '(id INT NOT NULL AUTOINCREMENT,' \
           ' cpcode CHAR(50) NOT NULL,' \
           ' interrupt_time CHAR(50),' \
           ' restore_time CHAR(50),' \
           ' event_age CHAR(50));'
    cursor.execute(sql1)
    cursor.execute(sql2)
    cursor.execute(sql3)
    # sql4 = 'CREATE UNIQUE INDEX statue_index ON c_state_latest(cpcode);'
    # cursor.execute(sql4)
    conn.commit()
    conn.close()


if __name__ == '__main__':

    print('***************')
    len(sys.argv)
    os.popen('echo {} >> /home/zabbix/1.log'.format(str(sys.argv)))

    path = os.getcwd()
    file_list = os.listdir(path)
    db_flag = 0
    for i in file_list:
        if 'bestTV.db' in i:
            print('数据库已存在')
            db_flag = 1
            break

    if db_flag == 0:
        db_exist(path)
    conn = sqlite3.connect(path+'/bestTV.db')
    cursor = conn.cursor()

    if sys.argv[-1] == 'restore':
        res_time = sys.argv[1]
        cpcode = sys.argv[3]
        event_age = sys.argv[5]

        # sql1 = f'INSERT INTO ch_event(cpcode,restore_time,event_age) VALUE({cpcode},{res_time},{event_age});'
        sql1 = 'INSERT INTO ch_event(cpcode,restore_time,event_age) VALUES("{}","{}","{}");'.format(cpcode,res_time,event_age)
        os.popen('echo {} >> /home/zabbix/1.log'.format(sql1))
        sql2 = 'INSERT INTO c_state_latest(cpcode,state)VALUES("{}","1") ON DUPLICATE KEY UPDATE cpcode="{}";'.format(cpcode, cpcode)
        cursor.execute(sql1)
        cursor.execute(sql2)
        conn.commit()
        conn.close()

    if sys.argv[-1] == 'interrupt':
        pass