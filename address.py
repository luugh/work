#!/usr/bin/python
# -*- coding:utf-8 -*-
import codecs


def get_area():
    address = {}
    try:
        with codecs.open('./address.txt', 'r', encoding='GB2312') as f:

            for line in f:
                line = line.strip()
                # print(line)
                if not len(line):
                    continue
                address[line.split(':')[0]] = line.split(':')[1]
            # print(address)
    except IOError as err:
        print('Please confirm whether channels. TXT exists')
    return address


def get_bundwidth():
    bundwidth = {}
    try:
        with open('./bundwidth.txt', 'r') as f:

            for line in f:
                line = line.strip()
                if not len(line):
                    continue
                bundwidth[line.split(':')[0]] = line.split(':')[1]
            # print(channels)
    except IOError as err:
        print('Please confirm whether channels. TXT exists')
    return bundwidth


def get_iplist(pwd):
    iplist = []
    try:
        with codecs.open(pwd, 'r') as f:

            m = 0
            for line in f:
                line = line.strip()
                # print(line)
                if not len(line):
                    continue
                if m > 1:
                    iplist.append(line)
                m = m + 1
            # print(address)
    except IOError as err:
        print('Please confirm whether channels. TXT exists')
    return iplist
