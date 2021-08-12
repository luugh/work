#!/usr/bin/python
# -*- coding:utf-8 -*-
import re, pymysql, os
from multiprocessing.dummy import Pool
from address import get_area
from address import get_bundwidth
from address import get_iplist

chanlist = []
sportch = []
sportsn = []
allch = []
allsn = []


def ip_sql(hosts):
    with open('/home/worldcup/tvmark', 'r') as f:
        for i in f:
            tv = '\"' + i.replace('\n', '').strip() + '\"'
            chanlist.append(tv)
    pot = ','
    tvstr = pot.join(chanlist)

    fileslist = os.listdir(hosts)
    for i in fileslist:
        pwd = hosts + i
        with open(pwd, 'r') as f:
            timedict = {}
            dictspch = {}
            dictspsn = {}
            dictallch = {}
            dictallsn = {}
            for i in f:
                str = i.replace('\n', '')
                s = re.match('startime=(.*)', str)
                e = re.match('endtime=(.*)', str)
                if s:
                    timedict["startime"] = s.group(1)
                elif e:
                    timedict["endtime"] = e.group(1)
                else:
                    ip = str
                    sportsql = 'select count(media_name) from cdr where media_name in (' + tvstr + \
                               ') and insertTime between \"' + timedict["startime"] + '\" and \"' + timedict["endtime"]\
                               + '\";'
                    alltvsql = 'select count(media_name) from cdr where insertTime between \"' + timedict["startime"] +\
                               '\" and \"' + timedict["endtime"] + '\";'
                    sportsnsql = 'select count(distinct(client_sn)) from cdr where media_name in (' + tvstr +\
                                 ') and insertTime between \"' + timedict["startime"] + '\" and \"' + \
                                 timedict["endtime"] + '\";'
                    allsnsql = 'select count(distinct(client_sn)) from cdr where insertTime between \"' + \
                               timedict["startime"] + '\" and \"' + timedict["endtime"] + '\";'
                    # print alltvsql
                    # print sportsql
                    # print allsnsql
                    # print sportsnsql
                    dictspch = {ip: sportsql}
                    sportch.append(dictspch)

                    dictspsn = {ip: sportsnsql}
                    sportsn.append(dictspsn)

                    dictallch = {ip: alltvsql}
                    allch.append(dictallch)

                    dictallsn = {ip: allsnsql}
                    allsn.append(dictallsn)


# for i in sportsn:
#    for x in  i.items():
#      print x[0]

def select(list):
    result = []
    for i in list:
        for x in i.items():
            ip = x[0]
            sql = x[1]
            # print (ip)
            # print (sql)
            db = pymysql.connect(ip, "root", "Star.123Mysql", "cdn_log_system")
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            db.close()
            num = data[0][0]
            result.append(str(num))
            # print ("%s\t%s\t%s\t%s" %(area[ip],ip,num,bandwidth[ip]))
            # print(area[ip] + '\t' + ip + '\t' + str(num) + '\t' + bandwidth[ip])
            # resultdic={ip:num}
            # listfinall.append(resultdic)
    return result


if __name__ == '__main__':
    chanlist = []
    sportch = []
    sportsn = []
    allch = []
    allsn = []
    area = get_area()
    bandwidth = get_bundwidth()
    hosts = '/home/worldcup/host/'
    timedict = {}
    ip_sql(hosts)
    print("sport_channle_num")
    sport_channle_num = []
    sport_channle_num.extend(select(sportch))
    print(len(sport_channle_num))

    # print(sport_channle_num)
    print("all_channle_num")
    all_channle_num = []
    all_channle_num.extend(select(allch))
    print(len(all_channle_num))

    print("sport_sn_num")
    sport_sn_num = []
    sport_sn_num.extend(select(sportsn))
    print(len(sport_sn_num))

    print("allsn")
    allsn_num = []
    allsn_num.extend(select(allsn))

    print(len(allsn_num))

    ip_list =[]
    print('ip_list')
    ip_list.extend(get_iplist(pwd='/home/worldcup/host/meiguo'))
    ip_list.extend(get_iplist(pwd='/home/worldcup/host/ouzhou'))
    print(len(ip_list))

    m = 0
    print('地区' + '\t' + 'CDN' + '\t' + 'sport_channle_num' + '\t' + 'all_channle_num' + '\t' + "sport_sn_num" + '\t' +
          "allsn" + '\t' + '带宽')
    for ip in ip_list:
        print(area[ip] + '\t' + ip + '\t' + sport_channle_num[m] + '\t' + all_channle_num[m] + '\t' + sport_sn_num[m] +
              '\t' + allsn_num[m] + '\t' + bandwidth[ip])
        # print(area[ip] + '\t' + ip + '\t' + str(num) + '\t' + bandwidth[ip])
        m = m + 1
