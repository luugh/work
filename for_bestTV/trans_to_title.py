# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2021/1/27 11:33
# @Author  : LGH
# @File    : trans_to_title.py
# @Software: PyCharm


import os


def trans():
    with open(r'.\name.txt', 'r') as f:
        list = f.readlines()
    with open(r'.\name_result.txt', 'w+') as f:
        for l in list:
            print(l.strip().title().replace(' Hd', ' HD').replace(' Tv', ' TV'))
            f.write('{}\n'.format(l.strip().title().replace(' Hd', ' HD').replace(' Tv', ' TV').replace('Fhd', 'FHD')))
            # f.write('\n')


if __name__ == '__main__':
    trans()