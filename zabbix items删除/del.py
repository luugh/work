#!/usr/bin python3
# -*- encoding: utf-8 -*-

import json, sys, argparse
from zabbix_api import ZabbixAPI

server = "http://208.81.204.10:8000/zabbix"
username = "郭涛"
password = "mkcc151"
zapi = ZabbixAPI(server=server, path="", log_level=0)
zapi.login(username, password)

# 解析参数
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", help="host name")
    args = parser.parse_args()
    if not args.host:
        args.host = input('host: ')
    print(args)
    return args


# 根据hostname查询hostid
def get_host_id(host):
    print(host)
    host_l = host.split(',')
    print(host_l)
    get_host_id = zapi.host.get(
        {
            "output": "hostid",
            "filter": {
                "host": host_l
            }
        }
    )
    host_id = []
    print(get_host_id)
    host_id.append([I['hostid'] for I in get_host_id])
    print(host_id)
    return host_id[0]


# 查询host中所有item存入item_id列表中
def get_host_item(hosts_id):
    get_item_id = zapi.item.get(
        {
            "output": ["itemid", "key_"],
            "hostids": hosts_id,
            #            "filter": {
            #                "host":host.split(",")
        }
    )
    item_id = []
    item_id.append([I['itemid'] for I in get_item_id])
    print(item_id)
    return item_id[0]


# 删除host
def delete_host(hosts_id):
    hosts_delete = zapi.host.delete(hosts_id)
    return "host delete success!"


# 删除host中item
def delete_host_item(itemid):
    hosts_delete = zapi.item.delete(itemid)
    return "host_item " + itemid[0] + " delete success!"


if __name__ == "__main__":
    args = get_args()
    print('获取hostid')
    host_id = get_host_id(args.host)
    print('获取host_item')
    item_id = get_host_item(host_id)
    # 此处的for循环是将列表中所有元素全部单个定义为新的列表，然后调取api删除，因为一次5w个item的列表，api请求会超时。
    for i in range(len(item_id)):
        itemid = []
        itemid.append(item_id[i])
        print(item_id[i])
        # print(delete_host_item(itemid))
    # print(delete_host(host_id))
