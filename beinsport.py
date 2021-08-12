# -*- coding: utf-8 -*-

# 获取节目预告

import urllib.request
import datetime
from bs4 import BeautifulSoup
import xlrd, xlwt
import os

#获取网页内容
def geturl(day):
    url = "http://www.foxplaybrasil.com.br/listings/"+day
    data  = urllib.request.urlopen(url).read()
    #data_str  = data.decode('UTF-8')
    return  data
'''
    f = open("./bein.log","wb")
    f.write(bytes(str,"UTF-8"))
    f.close()
    #print (geturl("2017-01-20"))
'''
def creat_excel(name1,time_start,time_end,excel_name):#创建excle并写入数据
    f = xlwt.Workbook(name1)
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    title = ['预告名称','开始时间','结束时间','系统录制文件保存天数','是否允许系统录制','TVOD计费方式','TVOD计费单位',' ','是否允许个人录制',
             '个人录制计费方式','个人计费单位','个人录制价格','预告简介']
    n=0
    for title1 in title:
        sheet1.write(0,n,title1)
        n = n + 1
    n = 0
    for name in name1:
        sheet1.write(1+n,0,name)#预告名称
        sheet1.write(1+n,12,name)#预告简介
        n = n + 1

    n=0
    for timestart in time_start:
        sheet1.write(1+n,1,timestart)#开始时间
        n=n+1
    n=0
    for timeend in time_end:
        sheet1.write(1+n,2,time_end[n])#结束时间
        n = n+1
    n = 0
    for timeend in time_end:
        sheet1.write(1+n,3,'3')#系统录制文件保存天数
        sheet1.write(1+n,4,'1')#是否允许系统录制
        sheet1.write(1+n,5,'0')#TVOD计费方式
        sheet1.write(1+n,6,'1')#TVOD计费单位
        sheet1.write(1+n,7,'0')#
        sheet1.write(1+n,8,'0')#是否允许个人录制
        sheet1.write(1+n,9,'0')#个人录制计费方式
        sheet1.write(1+n,10,'0')#个人计费单位
        sheet1.write(1+n,11,'0')#个人录制价格
        #sheet1.write(1+n,12,'1')#预告简介
        n = n + 1
    f.save('./'+excel_name+'.xls')

if __name__ == '__main__':
    Fox_name = [];Fox_start = [];Fox_end = []
    Foxhd_name = [];Foxhd_start = [];Foxhd_end = []
    Fox1_name = [];Fox1_start = [];Fox1_end = []
    Foxaction_name = [];Foxaction_start = [];Foxaction_end = []
    Foxlife_name = [];Foxlife_start = [];Foxlife_end = []
    Foxlifehd_name = [];Foxlifehd_start = [];Foxlifehd_end = []
    Foxsports_name = [];Foxsports_start = [];Foxsports_end = []
    Foxsports2_name = [];Foxsports2_start = [];Foxsports2_end =[]
    Foxsports2hd_name = [];Foxsports2hd_start = [];Foxsports2hd_end =[]
    Foxsportshd_name = [];Foxsportshd_start = [];Foxsportshd_end =[]
    Fx_name = [];Fx_start = [];Fx_end = []
    Fxhd_name = [];Fxhd_start = [];Fxhd_end = []
    Natgeo_name = [];Natgeo_start = [];Natgeo_end = []
    Natgeohd_name = [];Natgeohd_start = [];Natgeohd_end = []
    Natgeowildhd_name =[];Natgeowildhd_start = [];Natgeowildhd_end = []
    Natgeowild_name = [];Natgeowild_start = [];Natgeowild_end = []

    today = datetime.date.today()#获取当前日期
#print(endday)
#for循环获取日期
    for i in range (0,7):
        targetday = today + datetime.timedelta(days = i)
        targetday_str = str(targetday)#当前日期字符串格式
        #print(targetday_str)
        data = geturl(targetday_str)
        print('获取'+targetday_str+'日节目预告成功')
        soup = BeautifulSoup(data,"html.parser")
        #对获取的网页进行处理，截取频道标签
        channel_name = ['row fox fox foxhd series','row fox-hd fox foxhd series','row fox1 foxmais F1BM default',
                        'row fox-action foxmais FABM default','row fox-life fox-life FL BRA lifestyle',
                        'row fox-life-hd fox-life FL BRA lifestyle','row fox-sports fox-sports foxsports sports',
                        'row fox-sports-2 fox-sports-2 foxsports2 sports','row fox-sports-2-hd fox-sports-2 foxsports2 sports',
                        'row fox-sports-hd fox-sports foxsports sports','row fx fx fxhd series','row fx-hd fx fxhd default',
                        'row nat-geo nat-geo NG BRA factual','row nat-geo-hd nat-geo NG BRA factual',
                        'row nat-geo-wild-hd  NGW BRA factual','row nat-geo-wild  NGW BRA factual']
        for channel in channel_name:#按频道名称截取标签
            channel_tag = soup.find('div',class_ = channel) #截取频道名标签块
            program_name = []; program_namestr = []          #定义节目名list
            program_time = []; program_timestr = []          #定义时间list
            program_name = channel_tag.find_all('h2')       #提取所有节目名标签
            program_time = channel_tag.find_all('h4')       #提取所有时间标签
            for i in program_name:                         #去节目名标签
                program_namestr.append(i.string)
            program_timestr = [j.string for j in program_time]#去时间标签 01:10 / 03:10
            day1 = targetday_str.replace('-', '.')              #替换年月日中的-为.
            time_start = []; time_end = []
            for t in program_timestr:
                if t[0:5] < '07:00':
                    day2 = targetday + datetime.timedelta(days=1)
                    day2_str = str(day2)
                    day2str = day2_str.replace('-', '.')
                    time_start.append(day2str+' '+t[0:5]+':00')
                else :
                    time_start.append(day1+' '+ t[0:5]+':00')
                if t[-6:-1] < '07:00':
                    day2 = targetday + datetime.timedelta(days=1)
                    day2_str = str(day2)
                    day2str = day2_str.replace('-', '.')
                    time_end.append(day2str+' '+t[-6:-1]+':00')
                else:
                    time_end.append(day1+' '+t[-6:-1]+':00')
            if channel == 'row fox fox foxhd series':
                for name in program_namestr:
                    Fox_name.append(name)
                for timestart in time_start:
                    Fox_start.append(timestart)
                for timeend in time_end:
                    Fox_end.append(timeend)
            elif channel == 'row fox-hd fox foxhd series':
                for name in program_namestr:
                    Foxhd_name.append(name)
                for timestart in time_start:
                    Foxhd_start.append(timestart)
                for timeend in time_end:
                    Foxhd_end.append(timeend)
            elif channel == 'row fox1 foxmais F1BM default':
                for name in program_namestr:
                    Fox1_name.append(name)
                for timestart in time_start:
                    Fox1_start.append(timestart)
                for timeend in time_end:
                    Fox1_end.append(timeend)
            elif channel == 'row fox-action foxmais FABM default':
                for name in program_namestr:
                    Foxaction_name.append(name)
                for timestart in time_start:
                    Foxaction_start.append(timestart)
                for timeend in time_end:
                    Foxaction_end.append(timeend)
            elif channel == 'row fox-life fox-life FL BRA lifestyle':
                for name in program_namestr:
                    Foxlife_name.append(name)
                for timestart in time_start:
                    Foxlife_start.append(timestart)
                for timeend in time_end:
                    Foxlife_end.append(timeend)
            elif channel == 'row fox-life-hd fox-life FL BRA lifestyle':
                for name in program_namestr:
                    Foxlifehd_name.append(name)
                for timestart in time_start:
                    Foxlifehd_start.append(timestart)
                for timeend in time_end:
                    Foxlifehd_end.append(timeend)
            elif channel == 'row fox-sports fox-sports foxsports sports':
                for name in program_namestr:
                    Foxsports_name.append(name)
                for timestart in time_start:
                    Foxsports_start.append(timestart)
                for timeend in time_end:
                    Foxsports_end.append(timeend)
            elif channel == 'row fox-sports-2 fox-sports-2 foxsports2 sports':
                for name in program_namestr:
                    Foxsports2_name.append(name)
                for timestart in time_start:
                    Foxsports2_start.append(timestart)
                for timeend in time_end:
                    Foxsports2_end.append(timeend)
            elif channel == 'row fox-sports-2-hd fox-sports-2 foxsports2 sports':
                for name in program_namestr:
                    Foxsports2hd_name.append(name)
                for timestart in time_start:
                    Foxsports2hd_start.append(timestart)
                for timeend in time_end:
                    Foxsports2hd_end.append(timeend)
            elif channel == 'row fox-sports-hd fox-sports foxsports sports':
                for name in program_namestr:
                    Foxsportshd_name.append(name)
                for timestart in time_start:
                    Foxsportshd_start.append(timestart)
                for timeend in time_end:
                    Foxsportshd_end.append(timeend)
            elif channel == 'row fx fx fxhd series':
                for name in program_namestr:
                    Fx_name.append(name)
                for timestart in time_start:
                    Fx_start.append(timestart)
                for timeend in time_end:
                    Fx_end.append(timeend)
            elif channel == 'row fx-hd fx fxhd default':
                for name in program_namestr:
                    Fxhd_name.append(name)
                for timestart in time_start:
                    Fxhd_start.append(timestart)
                for timeend in time_end:
                    Fxhd_end.append(timeend)
            elif channel == 'row nat-geo nat-geo NG BRA factual':
                for name in program_namestr:
                    Natgeo_name.append(name)
                for timestart in time_start:
                    Natgeo_start.append(timestart)
                for timeend in time_end:
                    Natgeo_end.append(timeend)
            elif channel == 'row nat-geo-hd nat-geo NG BRA factual':
                for name in program_namestr:
                    Natgeohd_name.append(name)
                for timestart in time_start:
                    Natgeohd_start.append(timestart)
                for timeend in time_end:
                    Natgeohd_end.append(timeend)
            elif channel == 'row nat-geo-wild-hd  NGW BRA factual':
                for name in program_namestr:
                    Natgeowildhd_name.append(name)
                for timestart in time_start:
                    Natgeowildhd_start.append(timestart)
                for timeend in time_end:
                    Natgeowildhd_end.append(timeend)
            elif channel == 'row nat-geo-wild  NGW BRA factual':
                for name in program_namestr:
                    Natgeowild_name.append(name)
                for timestart in time_start:
                    Natgeowild_start.append(timestart)
                for timeend in time_end:
                    Natgeowild_end.append(timeend)
    print('开始写入表格：')
    creat_excel(Fox_name,Fox_start,Fox_end,'Fox')
    print('编辑 Fox 成功')
    creat_excel(Foxhd_name,Foxhd_start,Foxhd_end,'Fox HD')
    print('编辑 Fox HD 成功')
    creat_excel(Fox1_name,Fox1_start,Fox1_end,'Fox 1')
    print('编辑 Fox 1 成功')
    creat_excel(Foxaction_name,Foxaction_start,Foxaction_end,'Fox Action')
    print('编辑 Fox Action 成功')
    creat_excel(Foxlife_name,Foxlife_start,Foxlife_end,'Fox Life')
    print('编辑 Fox Life 成功')
    creat_excel(Foxlifehd_name,Foxlifehd_start,Foxlifehd_end,'Fox Life HD')
    print('编辑 Fox Life HD 成功')
    creat_excel(Foxsports_name,Foxsports_start,Foxsports_end,'Fox Sports')
    print('编辑 Fox Sports 成功')
    creat_excel(Foxsports2_name,Foxsports2_start,Foxsports2_end,'Fox Sports 2')
    print('编辑Fox Sports 2 成功')
    creat_excel(Foxsports2hd_name,Foxsports2hd_start,Foxsports2hd_end,'Fox Sports 2 HD')
    print('编辑 Fox Sports 2 HD 成功')
    creat_excel(Foxsportshd_name,Foxsportshd_start,Foxsportshd_end,'Fox Sports HD')
    print('编辑 Fox Sports HD 成功')
    creat_excel(Fx_name,Fx_start,Fx_end,'Fx')
    print('编辑 Fx 成功')
    creat_excel(Fxhd_name,Fxhd_start,Fxhd_end,'Fx HD')
    print('编辑 Fx HD 成功')
    creat_excel(Natgeo_name,Natgeo_start,Natgeo_end,'Nat Geo')
    print('编辑 Nat Geo 成功')
    creat_excel(Natgeohd_name,Natgeohd_start,Natgeohd_end,'Nat Geo HD')
    print('编辑 Nat Geo HD 成功')
    creat_excel(Natgeowild_name,Natgeowild_start,Natgeowild_end,'Nat Geo Wild')
    print('编辑 Nat Geo Wild 成功')
    creat_excel(Natgeowildhd_name,Natgeowildhd_start,Natgeowildhd_end,'Nat Geo Wild HD')
    print('编辑 Nat Geo Wild HD 成功')