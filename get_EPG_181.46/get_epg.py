#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import datetime
import json
import sys

url = "http://198.16.64.83:7016/live_sync"

response = requests.get(url)
content = response.text
print(content)
print(response.status_code)
# list1 = content['Spiderdata']
# # print(content['Spiderdata'])
# # print(type(content))
# data = {}
# for i in list1:
#     data[i['webtype']]=i['addtime']
# # print(data)
# data2 = []
# if len(sys.argv) == 1:
#     for t in data.keys():
#         # print(t)
#         data2.append('{"{#CHNAME}":"'+t+'"}')
#     data21 = str(data2).replace("'", "")
#     json = '{"data":'+data21+'}'
#     print(json)
#     # print(data.keys())
# else:
#     webtype = str(sys.argv[1])
#     print(data[webtype])
