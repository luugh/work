# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@File    :  swedish_links.py  
@Software:  PyCharm
@Modify Time:   2019/8/8 10:11
@Author:    LGH
@Version    
@Desciption
------------      -------    --------    -----------
'''

import difflib

def get_equal_rate(str1, str2):
    difflib.SequenceMatcher(None, a, b).ratio()