# !/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql
import openpyxl


class MyDb:
    def __init__(self):
        self.name = 'monitor'
        self.passwd = 'monitor2016'
        self.dbname = 'glist'
        self.port = '3306'


    def connect_db(self, host):
        db = pymysql.connect(host, self.name, self.passwd, self.dbname)
        return db

    def get_vis(self, connect_db):
        cursor = connect_db.cursor()
        # select_command = 'SELECT media_name,COUNT(media_name)from cdr where insertTime BETWEEN "2019-06-01 20:00:00" ' \
        #                  'AND "2019-06-01 23:00:00" AND (media_name like "%TV4001%" OR media_name like "%TV4002%"' \
        #                  'OR media_name like "%TV4003%" OR media_name like "%TV4011%" OR media_name like "%TV3167%") ' \
        #                  'AND response_code = "200"' \
        #                  'AND play_duration > "60"' \
        #                  'GROUP BY media_name'
        # select_command1 = 'SELECT COUNT(media_name) from cdr where insertTime BETWEEN "2019-06-01 20:00:00"' \
        #                   'AND "2019-06-01 23:00:00" ' \
        #                   'AND response_code = "200"' \
        #                   'AND play_duration > "60"'
        select_command = r'SELECT COUNT("TV3861") from gl_program_month_view  where month = "2019-09"'
        cursor.execute(select_command)
        results = cursor.fetchall()
        # cursor.execute(select_command1)
        # results1 = cursor.fetchall()
        # print(results1)
        # print(type(results))
        # print(results)
        # ip_list = []
        # for i in results:
        #     ip_list.append(i[0])
        # print(ip_list)
        # 返回ip列表元组
        return results


    def close(self, connect_db):
        connect_db.close()



if __name__ == "__main__":

    ip_list =
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
