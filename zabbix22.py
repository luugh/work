#-*- coding:UTF-8 -*-

import requests

url = 'http://119.146.223.77:8000/zabbix/index.php'

header1 = {
'Accept' : 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
'Connection':'keep-alive',
'Content-Length':"89",
'Content-Type':	"application/x-www-form-urlencoded",
'Cookie':'PHPSESSID=2ocf0dn87h2352iij8fon4qrr7',
'Host':	'119.146.223.77:8000',
'Referer':'http://119.146.223.77:8000/zab….php%3Faction%3Ddashboard.view',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/61.0'

}

body = b'form_refresh=1&name=%E5%88%98%E5%86%A0%E5%8D%8E&password=123456&autologin=1&enter=Sign+in'

r = requests.session()
res= r.post(url=url, data=body)
resp = r.get('http://119.146.223.77:8000/zabbix/zabbix.php?action=dashboard.view')
print(res.status_code)
print(res.text)

