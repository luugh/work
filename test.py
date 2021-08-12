#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd,xlutils
import pymysql
'''
classmates = [1,2,3,'szm','zx']
print (classmates)
print(classmates[len(classmates) - 1])
print (len(classmates))
print (type (len(classmates)) )
classmates.append('添加到尾部')
print(classmates)
classmates.insert(1,'插入到位置1')
print(classmates)
classmates.pop() #删除尾部元素
print(classmates,'删除尾部元素')
classmates.pop(1)
print(classmates,'删除指定位置1的元素')

# -*- coding: utf-8 -*-

L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Lisa']
]
print(L[0][0])
print(L[1][1])
print(L[2][2])
age = 19
print(age)

height = 1.75
weight = 80.5
bmi = 75 / ( 1.70*1.70 )
print ( bmi )
if bmi < 18.5:
    print ( "过轻" )
elif bmi < 25:
    print("正常")
elif bmi < 28:
    print("过重")
elif bmi < 32:
    print('肥胖')
else:
    print('严重肥胖')

s = input('input')
print (s)

L = ['Bart', 'Lisa', 'Adam']

for name in L:
    print ('hello,',name,'!')

for x in range (1,10 ):
    print(x)

print (2**3)

n1 = 255
n2 = 1000
print (str(hex(n1)))
print (str(hex(n2)))

import math
def quadratic(a,b,c):
    if (b**2 - 4*a*c) >= 0:
        x1 = (-b +math.sqrt((b**2 - 4*a*c)) )/(2*a)
        x2 = (-b -math.sqrt((b**2 - 4*a*c)) )/(2*a)
        return x1,x2

    else:
        return('b*b - 4*a*c < 0')

print(quadratic(1,9,5))

#默认参数
def power (x,n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
print(power(5,3))

import re
link = re.compile("\d+")
content = "loawang-233haha"
info = re.sub(link,'697',content)
print (info)

#尾递归
def fact_iter(n):
    return fact_iter(n,1)
def fact_iter(num,product):
    if num == 1:
        return product
    return fact_iter(num -1 ,num * product)
print(fact_iter(5,1))

#汉诺塔
def move(n,a,b,c):
    if n == 1:
        print('move', a, '--->', c)
        return
    move(n-1,a,c,b)
    print('move',a,'--->',c)
    move(n-1,b,a,c)
move(5,'A','B','C')


L = [i for i in range(7)]
print(L)

for i in range(6):
    print (i)

l = {"12":"65"}
print (l)

def test(a,b):
    c = []
    d = []
    c = a + [1,2]
    d = b + [1,2]
    return c,d
c = [3,4]
d = [3,4]
e = [5,6]
f = [7,8]
test (c,d)
print (test(e,f))

t = '01:10 / 03:10 '
print(t[0:5],t[-5:-1])
print (t[0:5] < t[-7:-1])
print(t[0:5]< '06:00')
print('12:00'<'06:00')
'''
'''
import datetime
#字符串转化为时间
x = datetime.datetime.strptime('2017.03.06 01:00:00', '%Y.%m.%d %H:%M:%S')
print(x)
y = x + datetime.timedelta(hours=8)
print(y)
print(type(y))
#时间转化为字符串
date_str = datetime.datetime.strftime(y, '%Y.%m.%d %H:%M:%S')
print(date_str)
print(type(date_str))
'''
'''
l = [1,2,3,4,'']

dellist = []

for i in l:

    if i == '':

        dellist.append(i)
        print(dellist)
for i in dellist:
    l.remove(i)
print(l)

import os,sys

url = 'http://georgeofthejungle.ddns.net:8000/live/mars/l97rC2zN1p/8109.ts'
f = open('C:/Users/Administrator/Desktop/vlc1.xspf', 'w')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
f.write('<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">\n')
f.write('	<title>播放列表</title>\n')
f.write('	<trackList>\n')
f.write('		<track>\n')
f.write('			<location>'+url+'</location>\n')
f.write('			<extension application="http://www.videolan.org/vlc/playlist/0">\n')
f.write('				<vlc:id>0</vlc:id>\n')
f.write('			</extension>\n')
f.write('		</track>\n')
f.write('	<extension application="http://www.videolan.org/vlc/playlist/0">\n')
f.write('			<vlc:item tid="0"/>\n')
f.write('	</extension>\n')
f.write('</playlist>\n')
f.close()
file = open('C:/Users/Administrator/Desktop/vlc1.xspf').read()
transfile = file.encode("UTF-8")
open('C:/Users/Administrator/Desktop/vlc1.xspf', 'wb+').write(transfile)


list = [1,2,3,4,5,6,]
length = len(list)
print (length)
n = 0
for i in range(0,length-1):
    print (list[n])
    n = n + 1

for line in open('channles.txt','r'):
    print (line)
    

for i in range(0,5):
    print (i)


lista = ('a', 'b')
listb = {'a':'cdf'}

print(listb[lista[0]])
      

db = pymysql.connect("185.53.11.159", "root", "Star.123Mysql", "mocean_cdn")
#db = pymysql.connect('221.4.223.105', 'monitor', 'monitor2016', 'glist')
cursor = db.cursor()
sql = "SELECT * FROM gslb_statistics WHERE channel_name = 'TV8101' AND record_time = '20170827*'"
#sql = "SELECT * FROM gl_program WHERE prog_id = 'TV8101' AND cdn_record_time > '20170827'"

m = cursor.execute(sql)

print(m)
print(type(m))
#n = cursor.fetchall()

#for i in n:
#    print(i)

db.close()



if 1:
    x=1
print(x)

n = 1
m = "server_" + str(n)
print(m)
print(type(m))
ip = "'127.0.0.1'"
login = ip+",'root','Star.123Mysql','cms'"
print(login)


login =''
db = pymysql.connect(host='192.168.8.106', user='root', passwd='Star.123Mysql', db='test', port=3306, charset='utf8')
cursor = db.cursor()
list1 = ("TV55", "TV40")
sql = 'update cms set server_1="root" where cpcontentid like "%%%s%%"'
print(sql)
cursor.executemany(sql, list1)
db.commit()
db.close()



import requests
import sys,io
import urllib.parse
import urllib.request
import time
import json
import pymysql

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

r = requests.get('http://www.haishilist.com:8180/cms/goLogin.action')
#print(r.headers['Set-Cookie'])
jsessionid= str(r.headers['Set-cookie']).split(';')[0]
print(jsessionid)
cookie = jsessionid + '; cms_language=zh_CN; loginUser=%E5%88%98%E5%86%A0%E5%8D%8E; loginPass=7Wg4ne6T8f;'

url = 'http://www.haishilist.com:8180/cms//channel/channelList.action?hasInput=N'


headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
                'Cookie': cookie,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'keep-alive'
           }

#login
post_login = urllib.parse.urlencode({
            'checkbox': '',
            'request_locale': 'en_US',
            'userName':	'刘冠华',
            'userPassword':	'7Wg4ne6T8f'
}).encode("utf-8")

#get
postdata = urllib.parse.urlencode({
             'broadcasttype': '-1',
             'ids': '',
             'page': '1',
             'qtype': '',
             'query': '',
             'releaseStatus': '2',
             'rp': '100',
             'servicbean.queryWords': '',
             'servicbean.status': '-1',
             'servicbean.type': '-1',
             'sortname':	'channelnumber',
             'sortorder': 'desc',
             'status': '0'
}).encode("utf-8")
#登录使cookie生效
req0 = urllib.request.Request(url='http://www.haishilist.com:8180/cms/login.action', data=post_login, headers=headers)
res0 = urllib.request.urlopen(req0)
#print(res0.read())
#res = requests.post(url=url,data=postadta,headers= headers)
req = urllib.request.Request(url=url, data=postdata, headers=headers)
#req = requests.post(url=url, data=postdata, headers=headers)
#print(req.text)
res = urllib.request.urlopen(req)
#print(res.read().decode('utf-8'))
ex = res
print(ex)
print(type(ex))

ex_list = json.load(ex)
print(ex_list)
print(ex_list['rows'][0]['id'])


#!/usr/bin/env python
import urllib.request
import urllib.parse
import json

#定义URL账户密码
url = 'http://119.146.223.77:8000/zabbix/index.php?request=zabbix.php%3Faction%3Ddashboard.view'
username = 'tmp'
password = '123456'

#定义通过HTTP方式访问API地址的函数，后面每次请求API的各个方法都会调用这个函数
def requestJson(url,values):
    data = urllib.parse.urlencode(values).encode('UTF-8')
    print(1)
    req = urllib.request.Request(url, data, {'Content-Type': 'application/json-rpc'})
    print(2)
    response = urllib.request.urlopen(req, data)
    print(3)
    print(response.read().decode('UTF-8'))
    res = response
    output = json.loads(res.read().decode('UTF-8'))
    print(output)
    try:
        message = output['result']
    except:
        message = output['error']['data']
        print(message)
        quit()
    return output['result']

#API接口认证的函数，登录成功会返回一个Token
def authenticate(url, username, password):
    values = {'jsonrpc': '2.0',
              'method': 'user.login',
              'params': {
                  'user': username,
                  'password': password
              },
              'id': '0'
              }
    idvalue = requestJson(url,values)
    return idvalue

#调用函数
if __name__ == '__main__':
    auth = authenticate(url, username, password)
print(auth)

'''
# from address import get_area
# from address import get_bundwidth
# area = get_area()
# bundwidth = get_bundwidth()
# print(area['208.98.10.227'])
# print(bundwidth)
# import os
# filepath = os.getcwd()+r'\test.txt'
# with open(filepath, 'r') as f:
#     lines = f.readlines()
# print(lines)
#
# name = lines[0].strip()
# print(name)
#
# from selenium import webdriver
# import time
#
# browser = webdriver.Chrome()
# browser.get(url='https://www.beinsports.com/en/tv-guide')
# time.sleep(20)
#
# filename = "bein.html"
#
# with open(filename, 'w', encoding='utf-8') as f:
#     f.write(browser.page_source)
#
# browser.close()

# coding=utf-8

# import turtle
# from datetime import *
#
#
# # 抬起画笔，向前运动一段距离放下
# def Skip(step):
#     turtle.penup()
#     turtle.forward(step)
#     turtle.pendown()
#
#
# def mkHand(name, length):
#     # 注册Turtle形状，建立表针Turtle
#     turtle.reset()
#     Skip(-length * 0.1)
#     # 开始记录多边形的顶点。当前的乌龟位置是多边形的第一个顶点。
#     turtle.begin_poly()
#     turtle.forward(length * 1.1)
#     # 停止记录多边形的顶点。当前的乌龟位置是多边形的最后一个顶点。将与第一个顶点相连。
#     turtle.end_poly()
#     # 返回最后记录的多边形。
#     handForm = turtle.get_poly()
#     turtle.register_shape(name, handForm)
#
#
# def Init():
#     global secHand, minHand, hurHand, printer
#     # 重置Turtle指向北
#     turtle.mode("logo")
#     # 建立三个表针Turtle并初始化
#     mkHand("secHand", 135)
#     mkHand("minHand", 125)
#     mkHand("hurHand", 90)
#     secHand = turtle.Turtle()
#     secHand.shape("secHand")
#     minHand = turtle.Turtle()
#     minHand.shape("minHand")
#     hurHand = turtle.Turtle()
#     hurHand.shape("hurHand")
#
#     for hand in secHand, minHand, hurHand:
#         hand.shapesize(1, 1, 3)
#         hand.speed(0)
#
#     # 建立输出文字Turtle
#     printer = turtle.Turtle()
#     # 隐藏画笔的turtle形状
#     printer.hideturtle()
#     printer.penup()
#
#
# def SetupClock(radius):
#     # 建立表的外框
#     turtle.reset()
#     turtle.pensize(7)
#     for i in range(60):
#         Skip(radius)
#         if i % 5 == 0:
#             turtle.forward(20)
#             Skip(-radius - 20)
#
#             Skip(radius + 20)
#             if i == 0:
#                 turtle.write(int(12), align="center", font=("Courier", 14, "bold"))
#             elif i == 30:
#                 Skip(25)
#                 turtle.write(int(i / 5), align="center", font=("Courier", 14, "bold"))
#                 Skip(-25)
#             elif (i == 25 or i == 35):
#                 Skip(20)
#                 turtle.write(int(i / 5), align="center", font=("Courier", 14, "bold"))
#                 Skip(-20)
#             else:
#                 turtle.write(int(i / 5), align="center", font=("Courier", 14, "bold"))
#             Skip(-radius - 20)
#         else:
#             turtle.dot(5)
#             Skip(-radius)
#         turtle.right(6)
#
#
# def Week(t):
#     week = ["星期一", "星期二", "星期三",
#             "星期四", "星期五", "星期六", "星期日"]
#     return week[t.weekday()]
#
#
# def Date(t):
#     y = t.year
#     m = t.month
#     d = t.day
#     return "%s %d%d" % (y, m, d)
#
#
# def Tick():
#     # 绘制表针的动态显示
#     t = datetime.today()
#     second = t.second + t.microsecond * 0.000001
#     minute = t.minute + second / 60.0
#     hour = t.hour + minute / 60.0
#     secHand.setheading(6 * second)
#     minHand.setheading(6 * minute)
#     hurHand.setheading(30 * hour)
#
#     turtle.tracer(False)
#     printer.forward(65)
#     printer.write(Week(t), align="center",
#                   font=("Courier", 14, "bold"))
#     printer.back(130)
#     printer.write(Date(t), align="center",
#                   font=("Courier", 14, "bold"))
#     printer.home()
#     turtle.tracer(True)
#
#     # 100ms后继续调用tick
#     turtle.ontimer(Tick, 100)
#
#
# def main():
#     # 打开/关闭龟动画，并为更新图纸设置延迟。
#     turtle.tracer(False)
#     Init()
#     SetupClock(160)
#     turtle.tracer(True)
#     Tick()
#     turtle.mainloop()
#
#
# if __name__ == "__main__":
#     main()

################################################
# import os
# import time
#
#
# def main():
#     content = '北京欢迎你为你开天辟地…………'
#     while True:
#         # 清理屏幕上的输出
#         os.system('cls')  # os.system('clear')
#         print(content)
#         # 休眠200毫秒
#         time.sleep(0.2)
#         content = content[1:] + content[0]
#
#
# if __name__ == '__main__':
#     main()
####################################################
# import random
#
#
# def generate_code(code_len=4):
#     """
#     生成指定长度的验证码
#
#     :param code_len: 验证码的长度(默认4个字符)
#
#     :return: 由大小写英文字母和数字构成的随机验证码
#     """
#     all_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     last_pos = len(all_chars) - 1
#     code = ''
#     for _ in range(code_len):
#         index = random.randint(0, last_pos)
#         code += all_chars[index]
#     return code
#
#
# if __name__ == '__main__':
#     print(generate_code())
#####################################################################################
# def main():
#     num = int(input('Number of rows: '))
#     yh = [[]] * num
#     print(yh)
#     for row in range(len(yh)):
#         yh[row] = [None] * (row + 1)
#         for col in range(len(yh[row])):
#             if col == 0 or col == row:
#                 yh[row][col] = 1
#             else:
#                 yh[row][col] = yh[row - 1][col] + yh[row - 1][col - 1]
#             print(yh[row][col], end='\t')
#         print()
#
#
# if __name__ == '__main__':
#     main()
######################################################

from itertools import product

# a=['1','2','3']
# b=['q','w','e']
# c=['f1','f2','f3']
#
# for i,s,d in product(a,b,c):
#     print(i+s+d)
#

##########################################################


