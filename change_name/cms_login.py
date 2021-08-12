#!/usr/bin/python3
# -*- coding:utf-8 -*-
# cms登录及查询，修改
# by lgh
import requests
import json
import time
import os


class Cms:

    def __init__(self, ip):
        self.ip = ip
        self.cookie = ''
        self.rows = {}

    def login(self):
        # get cookies
        ip = self.ip
        url = 'http://%s:8180/cms/login.action' % ip
        # print(url)
        re = requests.get(url)
        # print(re.headers)
        # print(type(re.headers['Set-Cookie']))
        jsession_id = re.headers['Set-Cookie']

        host = '%s:8081' % ip
        referer = 'http://%s:8180/cms/goLogin.action' % ip
        # cookie = jsession_id + ";cms_language=en_US; loginUser=%E5%88%98%E5%86%A0%E5%8D%8E; loginPass=zVFaXk37"
        self.cookie = jsession_id
        headers = {
            # 'Host': '178.132.6.62:8180',
            'Host': host,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': "text/css,*/*;q=0.1",
            'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            # 'Referer': 'http://178.132.6.62:8180/cms/goLogin.action',
            'Referer': referer,
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': self.cookie
        }

        login_url = 'http://%s:8180/cms/login.action' % ip
        filepath = os.getcwd()+'\login.txt'
        with open(filepath, 'r') as f:
            list = f.readlines()
        name = list[0].strip()
        passwd = list[1].strip()
        # name = 'admin'
        # passwd = 'Q5t0wRLN'
        login_post = {
            'request_local': 'en_US',
            'userName': name,
            'userPassword': passwd,
            'checkbox': ''
        }
        res = requests.post(url=login_url, data=login_post, headers=headers)

        # print(res.status_code)
        # print(res.text)
        # print(res.headers)
        # print(res.headers['date'])

    def select_ch(self, cpcode):

        headers = {
            'Host': '%s:8081' % self.ip,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://%s:8180/cms//servermonitor/channelrecordlist.action' % self.ip,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            # 'Content-Length': '113',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': self.cookie
        }

        select_post = {
            'page': '1',
            'rp': '15',
            'sortname': 'id',
            'sortorder': 'desc',
            'query': '',
            'qtype': '',
            'name': cpcode,
            'status': '',
            'activeStatus': '',
            'streamStatus': '',
            'OnDemandFlag': '',
            'mypage': '1'
        }
        select_url = 'http://%s:8180/cms//servermonitor/getChannelRecords.action' % self.ip
        res = requests.post(url=select_url, data=select_post, headers=headers)
        # print(res.text)
        # print(type(res.text))
        # res.text输出内容为字符串，需要转换为字典
        result = json.loads(res.text)
        id = result['rows'][0]['id']
        # 获取id
        post_data = {'id': id}
        select_url1 = 'http://%s:8180/cms//servermonitor/getChannelRecordById.action' % self.ip

        ress = requests.post(url=select_url1, data=post_data, headers=headers)
        result1 = json.loads(ress.text)
        self.rows = result1
        # print(self.rows)
        # 提取唯一标识
        cpcode = self.rows['cpcontentid']
        channel_name = self.rows['remark']
        if self.rows['streamStatus'] =='1':
            stream_status = '正常'
        else:
            stream_status = '中断'
        status = self.rows['statusStr']
        origin = self.rows['origin']
        source_url = self.rows['sourceurl']
        print(('频道名称：%s\n' % channel_name)+('频道唯一标识：%s\n' % cpcode)+('流状态：%s\n' % stream_status)
              +('下发状态：%s\n' % status)+('源链接%s\n' % source_url)+('正在使用的链接：%s\n' % self.rows['currenturl'])
              +('备注：%s\n' % origin)+("\n"))
        # print('频道名称：%s' % channel_name)
        # print('频道唯一标识：%s' % cpcode)
        # print('流状态：%s' % stream_status)
        # print('下发状态：%s' % status)
        # print('源链接%s' % source_url):
        # print('正在使用的链接：%s' % self.rows['currenturl'])
        # print('备注：%s' % origin)
        # print("\n")

    def updata_ch(self, tv_name=None, url=None, origin=None):
        headers = {
            'Host': '%s:8081' % self.ip,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Accept': '*/*',
            'Accept-Language': 'zh,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://%s:8180/cms//servermonitor/channelrecordlist.action' % self.ip,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            # 'Content-Length': '113',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': self.cookie
        }
        if tv_name is not None:
            self.rows['remark'] = tv_name
            print('更新名称')
        if url is not None:
            self.rows['sourceurl'] = url
            print('更新源url')
        if origin is not None:
            self.rows['origin'] = origin
            print('更新来源分组')
        # print(self.rows)
        updata_post = {
            'OnDemandFlag': self.rows['onDemandFlag'],
            'activeStatus': self.rows['activeStatus'],
            'broadcasttype': self.rows['broadcasttype'],
            'channelIds': self.rows['channelId'],
            'status': self.rows['status'],
            'applicationMointorId': self.rows['applicationMointorId'],
            'sourceurl': self.rows['sourceurl'],
            'storageduration': '',
            'addtype': '0',
            'name': self.rows['cpcontentid'],
            'remark': self.rows['remark'],
            'origin': self.rows['origin'],  # 来源分组
            'id': self.rows['id']
        }
        # print('updata_post:' + str(updata_post))
        update_url = 'http://%s:8180/cms//servermonitor/modifyChannelRecord.action' % self.ip

        res = requests.post(url=update_url, data=updata_post, headers=headers)
        # print(res.text)
        # status = 'false'
        if res.text == 'true':
            print(('------------------------------')+('%s上%s更新成功\n' % (self.ip, self.rows['cpcontentid']))
                  +('------------------------------\n'))
            # print('%s上%s更新成功' % (self.ip, self.rows['cpcontentid']))
            # print('------------------------------')
        else:
            print(('------------------------------')+('%s上%s更新失败\n' % (self.ip, self.rows['cpcontentid']))
                  +(res.text)+('\n------------------------------\n'))
            # print('%s上%s更新失败' % (self.ip, self.rows['cpcontentid']))
            # print(res.text)
            # print('------------------------------')
        time.sleep(1)
        return res.text


if __name__ == "__main__":
    real_ip = '91.215.159.240'
    c = Cms(real_ip)
    c.login()
    ch = 'TV5060'
    c.select_ch(ch)
    c.updata_ch(tv_name='bein test')
    c.select_ch(ch)

