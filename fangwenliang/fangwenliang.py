#!/usr/bin python3
# -*- encoding: utf-8 -*-
'''
@File    :   fangwenliang.py   
@Contact :   
@License :   

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/6/2 5:24   lgh        1.0         None
'''


import pymysql

class MyDb:
    def __init__(self):
        self.name = 'root'
        self.passwd = 'Star.123Mysql'
        self.dbname = 'cdn_log_system'
        self.port = '3306'


    def connect_db(self, host):
        db = pymysql.connect(host, self.name, self.passwd, self.dbname)
        return db

    def get_vis(self, connect_db):
        cursor = connect_db.cursor()
        select_command = 'SELECT media_name,COUNT(media_name)from cdr where insertTime BETWEEN "2019-06-01 20:00:00" ' \
                         'AND "2019-06-01 23:00:00" AND (media_name like "%TV4001%" OR media_name like "%TV4002%"' \
                         'OR media_name like "%TV4003%" OR media_name like "%TV4011%" OR media_name like "%TV3167%") ' \
                         'AND response_code = "200"' \
                         'AND play_duration > "60"' \
                         'GROUP BY media_name'
        select_command1 = 'SELECT COUNT(media_name) from cdr where insertTime BETWEEN "2019-06-01 20:00:00"' \
                          'AND "2019-06-01 23:00:00" ' \
                          'AND response_code = "200"' \
                          'AND play_duration > "60"'
        cursor.execute(select_command)
        results = cursor.fetchall()
        cursor.execute(select_command1)
        results1 = cursor.fetchall()
        # print(results1)
        # print(type(results))
        # print(results)
        # ip_list = []
        # for i in results:
        #     ip_list.append(i[0])
        # print(ip_list)
        # 返回ip列表元组
        return results,results1

    def close(self, connect_db):
        connect_db.close()


if __name__ == "__main__":
    ip_list = ['190.2.142.155',
                '190.2.145.151',
                '212.8.253.23',
                '178.132.6.60',
                '190.2.141.93',
                '212.8.243.139',
                '185.180.222.85',
                '185.180.222.89',
                '185.180.222.91',
                '190.2.154.163',
                '185.132.177.120',
                '177.54.158.17',
                '208.81.204.20',
                '178.132.6.60',
                '208.81.204.24']
    ip_list1 = ['177.54.158.17',
                '208.81.204.20',
                '208.81.204.24']
    a = MyDb()
    for ip in ip_list:
        print(ip)
        conn = a.connect_db(host=ip)
        ip_tuple, all_num = a.get_vis(conn)
        print("总数")
        print(all_num)
        print("具体")
        for i in ip_tuple:
            # print(i)
            num = len(i)
            print(i[0]+":"+str(i[1]))
        print('_________________________')
        a.close(conn)

