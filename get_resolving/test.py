#!/usr/bin python3
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Contact :   
@License :   

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/5/5 20:46   lgh        1.0         None
'''

import ffmpeg
import subprocess
import datetime
from ffmpy import FFmpeg

import json, sys, argparse
from zabbix_api import ZabbixAPI
server = "http://208.81.204.10:8000/zabbix"
username = "郭涛"
password = "mkcc151"
zapi = ZabbixAPI(server=server, path="", log_level=0)
zapi.login(username, password)

if __name__ == "__main__":
    # startime = datetime.datetime.now()
    # # info = ffmpeg.probe('http://190.2.141.93:8082/TV5062')
    # # print(info)
    #
    #
    # # url = 'http://190.2.141.93:8082/TV5062'
    # # command = 'ffprobe -loglevel quiet -print_format json -show_format -show_streams -i ' + url
    # # # print(command)
    # # result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # # out = result.stdout.read()
    # # # print(str(out))
    # # temp = str(out.decode('utf-8'))
    # # print(temp)
    # endtime = datetime.datetime.now()
    # print(endtime - startime)
    #
    # input_file = 'TV4202.1.ts'
    # output_file = 'TV4202_001.ts'
    #
    # ff = FFmpeg(inputs={input_file: None},
    #             outputs={output_file: '-ss 00:01:00 -to 00:02:00 -c copy -y'}
    # )
    # print(ff.cmd)
    # ff.run()
    # # print(out)
    # # print(err)

    host = '89server'
    print(host)
    get_host_id = zapi.host.get(
        {
            "output": "hostid",
            "filter": {
                "host": host.split(",")
            }
        }
    )
    host_id = []
    print(get_host_id)
    host_id.append([I['hostid'] for I in get_host_id])
    print(host_id)
    print( host_id[0])