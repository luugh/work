#!/usr/bin/python
#coding:utf-8

import xlrd,xlwt
import pymysql
import xlsxwriter
import datetime


def getsheetdate():
    file = r'./template.xlsx'
    workbook = xlrd.open_workbook(file)
    sheet = workbook.sheet_by_name('Sheet1')

    return sheet

def getnacode(sheet, col):
    namelist = []
    cpcodelist = []
    m = 1
    n = 0
    cols = sheet.col_values(col)
    for m in range(len(cols)):
        if sheet.cell_value(m, col) != '':
            namelist.append(sheet.cell_value(m, col))
            cpcodelist.append(sheet.cell_value(m, col+2))
            #print(sheet.cell_value(m, col))

        else:
            n = 1
    #print(namelist)
    #print(cpcodelist)
    return namelist, cpcodelist
    #print([sheet.cell_value(1, 3)])

def sumvisits():
    today = datetime.datetime.today()
    today_str = today.strftime('%Y-%m-%d')
    yestoday = today - datetime.timedelta(days=1)
    be_yetoday = today - datetime.timedelta(days=2)
    yestoday_str = yestoday.strftime('%Y-%m-%d')
    be_yetoday_str = be_yetoday.strftime('%Y-%m-%d')
    print('开始获取155上%s的访问数据' %yestoday_str)
    #获取155访问数据
    localhost = '177.54.158.155'
    name = 'root'
    passwd = 'Star.123Mysql'
    dbname = 'cdn_log_system'
    media_name = "TV2316"
    db = pymysql.connect(localhost, name, passwd, dbname)
    cursor = db.cursor()
    sql = 'SELECT media_name,COUNT(media_name) as count FROM `cdr` WHERE play_duration>1 and insertTime BETWEEN "'+ yestoday_str +' 00:00:00" and "'+ today_str +' 00:00:00" GROUP BY media_name order by count desc;'

    try:
       # print('开始获取访问数据')
        cursor.execute(sql)
        result = cursor.fetchall()
        #print(result)
    except Exception:
        print("Error: unable to fetch data")
    db.close()
    #print(result)
    m = len(result)
    dict155 = {}
    for i in range(m):
        dict155[result[i][0]] = result[i][1]
    #print(dict155)
    print('开始获取24上%s的访问数据'%yestoday_str)
    #获取148.24节目数据
    localhost = '177.54.148.24'
    name = 'root'
    passwd = 'Star.123Mysql'
    dbname = 'cdn_log_system'
    media_name = "TV2316"
    db = pymysql.connect(localhost, name, passwd, dbname)
    cursor = db.cursor()
    sql = r'SELECT media_name,COUNT(media_name) as count FROM `cdr` WHERE play_duration>1 and insertTime BETWEEN "'+ yestoday_str +' 00:00:00" and "'+ today_str +' 00:00:00" GROUP BY media_name order by count desc;'

    try:
       # print('开始获取访问数据')
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
    except Exception:
        print("Error: unable to fetch data")
    db.close()
    #print(result)
    m = len(result)
    dict24 = {}
    for i in range(m):
        dict24[result[i][0]] = result[i][1]
    #print(dict24)
    print('开始获取17上%s的访问数据'%yestoday_str)
    #获取158.17访问数据
    localhost = '177.54.158.17'
    name = 'root'
    passwd = 'Star.123Mysql'
    dbname = 'cdn_log_system'
    media_name = "TV2316"
    db = pymysql.connect(localhost, name, passwd, dbname)
    cursor = db.cursor()
    sql = r'SELECT media_name,COUNT(media_name) as count FROM `cdr` WHERE play_duration>1 and insertTime BETWEEN "'+ yestoday_str +' 00:00:00" and "'+ today_str +' 00:00:00" GROUP BY media_name order by count desc;'

    try:
       # print('开始获取访问数据')
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
    except Exception:
        print("Error: unable to fetch data")
    db.close()
    #print(result)
    m = len(result)
    dict17 = {}
    for i in range(m):
        dict17[result[i][0]] = result[i][1]
    #print(dict17)
    print('开始获取60上%s的访问数据'%yestoday_str)
    #获取6.60访问数据
    localhost = '178.132.6.60'
    name = 'root'
    passwd = 'Star.123Mysql'
    dbname = 'cdn_log_system'
    media_name = "TV2316"
    db = pymysql.connect(localhost, name, passwd, dbname)
    cursor = db.cursor()
    sql = r'SELECT media_name,COUNT(media_name) as count FROM `cdr` WHERE play_duration>1 and insertTime BETWEEN "'+ yestoday_str +' 05:00:00" and "'+ today_str +' 05:00:00" GROUP BY media_name order by count desc;'

    try:
        #print('开始获取访问数据')
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
    except Exception:
        print("Error: unable to fetch data")
    db.close()
    #print(result)
    m = len(result)
    dict60 = {}
    for i in range(m):
        dict60[result[i][0]] = result[i][1]
    #print(dict60)
    print('开始获取218上%s的访问数据'%yestoday_str)
    #获取149.218访问数据
    localhost = '192.99.149.218'
    name = 'root'
    passwd = 'Star.123Mysql'
    dbname = 'cdn_log_system'
    media_name = "TV2316"
    db = pymysql.connect(localhost, name, passwd, dbname)
    cursor = db.cursor()
    sql = r'SELECT media_name,COUNT(media_name) as count FROM `cdr` WHERE play_duration>1 and insertTime BETWEEN "'+ be_yetoday_str +' 23:00:00" and "' + yestoday_str + ' 23:00:00" GROUP BY media_name order by count desc;'

    try:
        #print('开始获取访问数据')
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
    except Exception:
        print("Error: unable to fetch data")
    db.close()
    #print(result)
    m = len(result)
    dict218 = {}
    for i in range(m):
        dict218[result[i][0]] = result[i][1]
    #print(dict218)

    list155 = list(dict155.keys())
    list24 = list(dict24.keys())
    list17 = list(dict17.keys())
    list60 = list(dict60.keys())
    list218 = list(dict218.keys())

    listall  = [list155, list24, list17, list218]
    #print(list155)
    #print(listall[0])
    dictall = dict60
    listdictall = list(dictall.keys())
    #判断每个列表的值是否存在于listall中
    for n in range(len(listall)):
        for i in listall[n]:
            if i in listdictall:
                if n == 0 :
                    dictall[i] = str(int(dictall[i])+int(dict155[i]))
                if n == 1 :
                    dictall[i] = str(int(dictall[i]) + int(dict24[i]))
                if n == 2 :
                    dictall[i] = str(int(dictall[i]) + int(dict17[i]))
                if n == 3 :
                    dictall[i] = str(int(dictall[i]) + int(dict218[i]))
            else :
                if n == 0 :
                    dictall[i] = dict155[i]
                if n == 1 :
                    dictall[i] = dict24[i]
                if n == 2 :
                    dictall[i] = dict17[i]
                if n == 3 :
                    dictall[i] = dict218[i]
                    #print(type(dict218[i]))

    #print(dictall)
    return dictall



if __name__ == "__main__":

    sheet = getsheetdate()
    #print(sheet)
    #get brazil
    brazil_name, brazil_cpcode = getnacode(sheet, 0)
    por_name, por_cpcode = getnacode(sheet, 5)
    spla_name, spla_cpcode = getnacode(sheet, 10)
    speu_name, speu_cpcode = getnacode(sheet, 15)

    dictall = sumvisits()
    listall = list(dictall.keys())
    workbook = xlsxwriter.Workbook(r'C:\Users\Administrator\Desktop\南美访问量\demon.xlsx')
    worksheet = workbook.add_worksheet()
    #写标题
    worksheet.write(0, 0, brazil_name[0])
    worksheet.write(0, 5, por_name[0])
    worksheet.write(0, 10, spla_name[0])
    worksheet.write(0, 15, speu_name[0])


    for num in range(1, len(brazil_name)):


        if brazil_cpcode[num] in listall:
            worksheet.write(num, 0, brazil_name[num])
            worksheet.write(num, 1, 'Portuguese')
            worksheet.write(num, 2, brazil_cpcode[num])
            worksheet.write(num, 3, int(dictall[brazil_cpcode[num]]))
        else:
            worksheet.write(num, 0, brazil_name[num])
            worksheet.write(num, 1, 'Portuguese')
            worksheet.write(num, 2, brazil_cpcode[num])
            worksheet.write(num, 3, 0)

    for num in range(1, len(por_name)):

        if por_cpcode[num] in listall:
            worksheet.write(num, 5, por_name[num])
            worksheet.write(num, 6, 'Portuguese')
            worksheet.write(num, 7, por_cpcode[num])
            worksheet.write(num, 8, int(dictall[por_cpcode[num]]))
        else:
            worksheet.write(num, 5, por_name[num])
            worksheet.write(num, 6, 'Portuguese')
            worksheet.write(num, 7, por_cpcode[num])
            worksheet.write(num, 8, 0)

    for num in range(1, len(spla_name)):

        if spla_cpcode[num] in listall:
            worksheet.write(num, 10, spla_name[num])
            worksheet.write(num, 11, 'Spanish')
            worksheet.write(num, 12, spla_cpcode[num])
            worksheet.write(num, 13, int(dictall[spla_cpcode[num]]))
        else:
            worksheet.write(num, 10, spla_name[num])
            worksheet.write(num, 11, 'Spanish')
            worksheet.write(num, 12, spla_cpcode[num])
            worksheet.write(num, 13, 0)

    for num in range(1, len(speu_name)):

        if speu_cpcode[num] in listall:
            worksheet.write(num, 15, speu_name[num])
            worksheet.write(num, 16, 'Spanish')
            worksheet.write(num, 17, speu_cpcode[num])
            worksheet.write(num, 18, int(dictall[speu_cpcode[num]]))
        else:
            worksheet.write(num, 15, speu_name[num])
            worksheet.write(num, 16, 'Spanish')
            worksheet.write(num, 17, speu_cpcode[num])
            worksheet.write(num, 18, 0)
    workbook.close()