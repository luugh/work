#!/usr/bin/python
# conding=urf-8

# 统计小语种

import pymysql
import datetime
import xlutils
import xlsxwriter

'''
def getchdata(time):
    db = pymysql.connect("185.53.11.159", "root", "Star.123Mysql", "mocean_cdn")
    #db = pymysql.connect('221.4.223.105', 'monitor', 'monitor2016', 'glist')
    #cursor = db.cursor()

    #sql = "SELECT * FROM gl_program WHERE prog_id = 'TV8101' AND cdn_record_time > '2017-08-27'"
    # sql = "SELECT * FROM gslb_statistics WHERE channel_name = "+ channel_name +" AND record_time > " + time
   sql = "SELECT * FROM gslb_statistics WHERE prog_id = 'TV8101' AND record_time > " + time

   # m = cursor.execute(sql)

    #print(m)

   # n = cursor.fetchall()

   # for i in n:
        print(i)

    db.close()

'''
# get time
if __name__ == '__main__':



    day1 = datetime.date.today()
    day2 = datetime.date.today() - datetime.timedelta(days=7)
    day3 = datetime.date.today() - datetime.timedelta(days=8)
    day4 = datetime.date.today() - datetime.timedelta(days=14)
    day4_1 = day4 - datetime.timedelta(days=1)                    # 用于查询时取到day4当天的的访问量
    day1_1 = day1 + datetime.timedelta(days=1)                    # 用于取到day1当天的访问量
    print(day1,day2,day3,day4)
    day1_str = str(day1)
    day2_str = str(day2)
    day3_str = str(day3)
    day4_str = str(day4)
    day4_1_str = str(day4_1)
    day1_1_str = str(day1_1)
    # print(day2_str)

    # 判断需要26号是本月还是上月
    print(day1_str[-1:2])
    if day1_str[-1:2] <= '9':
        mou = int(day1_str[5:7])
        if mou == 1:
            m_str = day1_str[0:5] + "12" + '-26'
        else:
            m_str = day1_str[0:5] + "0" + str(mou-1) + '-26'
        print(m_str)
    elif day1_str[-1, 2] > '26':
        m_str = day1_str[0:8] + '26'
        print(m_str)
    week1 = 0
    week2 = 0
    # 判断需要查询的表(由于表数据的关系始终不能查询到边界日期的访问数据,所以查询时取边界日期的前一天)
    if m_str >= day4_str and m_str <= day3_str:  # 从当前往前第2周包含26号
        # 上一个26号结尾的表
        datalist1 = "gl_program_" + day2_str.replace('-', '_')[0:7]
        print(datalist1)
        db = pymysql.connect('221.4.223.105', 'monitor', 'monitor2016', 'glist')
        cursor = db.cursor()
        sql = "SELECT * FROM " + datalist1 + " WHERE prog_id = 'TV8101' AND cdn_record_time > " + "'"+day4_1_str+"'"
        print(sql)
        m = cursor.execute(sql)
        sql = "SELECT * FROM gl_program WHERE prog_id = 'TV8101' AND cdn_record_time < " + "'"+day2_str+"'"
        n = cursor.execute(sql)
        # 第二周访问数据结果
        week2 = m + n
        print(week2)
        # 第一周数据查询
        sql = "SELECT * FROM gl_program WHERE prog_id = 'TV8101' AND cdn_record_time > " + "'" +day3_str+"'"
        week1 = cursor.execute(sql)

        print(week2)
        db.close()
    elif m_str >= day2_str and m_str <= day1_str:

        datalist2 = "gl_program_" + day2_str.replace('-', '_')[0:7]
        db = pymysql.connect('221.4.223.105', 'monitor', 'monitor2016', 'glist')
        cursor = db.cursor()
        # 查询第二周数据
        sql = "SELECT * FROM " + datalist2 + " WHERE prog_id = 'TV8101' AND cdn_record_time > " + "'"+day4_1_str +\
              "' AND cdn_record_time < " + "'" + day2_str + "'"
        week2 = cursor.execute(sql)

        # 查询第一周数据
        sql = "SELECT * FROM " + datalist2 + " WHERE prog_id = 'TV8101' AND cdn_record_time > " + "'" + day3_str + "'"
        m = cursor.execute(sql)
        sql = "SELECT * FROM gl_program WHERE prog_id = 'TV8101'"
        n = cursor.execute(sql)
        db.close()
        week1 = n + m
    else:
        db = pymysql.connect('221.4.223.105', 'monitor', 'monitor2016', 'glist')
        cursor = db.cursor()
        # 查询第二周数据
        sql = "SELECT * FROM gl_program WHERE prog_id = 'TV8101'AND cdn_record_time > " + "'"+day4_1_str +\
              "' AND cdn_record_time < " + "'" + day2_str + "'"
        week2 = cursor.execute(sql)
        # 第一周数据
        sql = "SELECT * FROM gl_program WHERE prog_id = 'TV8101'AND cdn_record_time > " + "'"+day3_str +\
              "' AND cdn_record_time < " + "'" + day1_1_str + "'"
        week1 = cursor.execute(sql)

    workbook = xlsxwriter.Workbook('小语种统计.xlsx')
    worksheet = workbook.add_worksheet(name1[0])


# 频道元组
    Tamils = ('Tamils', 'TV8101')
    Tamils_ch = {'TV8101': 'Discovery Channel Tamil Nadu'}
    Telugu = ('Telugu', 'TV8167', 'TV8145', 'TV8144', 'TV8166', 'TV8150', 'TV8857')
    Telugu_ch = {'TV8167': 'Channel WIN', 'TV8145': 'Jai Telangana TV', 'TV8144': 'TV 9 Telugu',
                 'TV8166': 'Bhaarat Today', 'TV8150': 'Mahaa News', 'TV8857': 'Star Maa HD'}