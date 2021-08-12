#!/usr/bin/python3.6
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.listdir('.'))
from interrupt_query import get_server


if __name__ == '__main__':

    # print os.listdir('.')
    # list_dir = os.listdir('.')
    # name = 'test.py'
    # print name
    # for i in list_dir:
    #     if name in i:
    #         print(1)
    #     else:
    #         print(0)
    print (os.getcwd())

    dict1 = get_server()
    print(dict1)
    cp_list = dict1.keys()
    print(cp_list)