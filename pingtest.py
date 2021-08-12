#!/usr/bin/python
# coding:utf-8

import os
import datetime



r = os.popen('ping -n 50 www.baidu.com')
info = r.readlines()
print(info)

