# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2021/1/29 16:44
# @Author  : LGH
# @File    : update_ch.py
# @Software: PyCharm

import sqlite3
import os
import openpyxl


class MySql:

    def __init__(self):
        pass

    def create(self):
        pass


def get_ch():
    dir_list = os.listdir()
    print(dir_list)
    for name in dir_list:
        if '第三方源' in name:
            source_file = name
    file_path = os.getcwd() + '/' +source_file
    w1 = openpyxl.load_workbook(file_path)
    sh_names = w1.sheetnames
    dict1 = {
        '印度': '185.79.153.34',
        '青蛙源_南美': '199.167.137.146',
        '葡语西语44': '185.79.153.44',
        'myHD': '154.54.220.98',
        'Telefoot': '185.79.153.34',
        'bestTV': '54.78.82.194',
        'bestTV备用': '212.8.243.139',
        'xcstream': '38.94.97.150'
    }


if __name__ == '__main__':
    get_ch()