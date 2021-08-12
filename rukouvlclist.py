#-*- coding:utf-8 -*-
#by lgh

import sys
import io
from urllib import request,parse
import http.cookiejar

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

header_dict = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}

login_url = 'http://www.haishilist.com:8180/cms/goLogin.action'

req = request.Request(url=login_url, headers=header_dict)
res = request.urlopen(req)
res = res.read()
print(res)

response = request.urlopen('http://www.haishilist.com:8180/cms/goLogin.action')


f = open('./url.txt','w')
f.write(response.text)
f.close()