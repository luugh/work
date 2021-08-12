#-*-coding:utf-8-*-


import datetime,os
import xlrd, xlwt
import xlutils
from xlutils.copy import copy

def firstrow(rsheet,r):#获取第一列数据
    first_row = []
    for n in range(1,r):
        first_row.append(rsheet.cell_value(n, 0))
    return first_row

def starttime(rsheet,r):#获取起始时间列
    second_row = []
    for n in range(1,r):
        second_row.append(rsheet.cell_value(n,1))
    return second_row

def endtime(rsheet,r):#获取结束时间列
    third_row = []
    for n in range(1,r):
        third_row.append(rsheet.cell_value(n,2))
    return third_row

#def changedate(timestr):#字符串转换时间
#    return datetime.datetime.strptime(timestr,'%Y.%m.%d %H:%M:%S')

def changetime(time, t):#时差
    timeend = time + datetime.timedelta(hours=t)
    #print('时间转换完成')
    return timeend

def deitexcle(rsheet,wsheet,r,ncol,time_change): #主体文件编辑,xlrd获取的表，复制的表，行数，列数，时差（小时）

                    #获取起始时间字符串
        time1str = starttime(rsheet, r)
        #for n in time1str:
        #    print(n)
        #    print(type(n))
        endtimestr = endtime(rsheet, r)
        #除去列表中的最后一个元素
        time1str.pop()
        endtimestr.pop()
        #time1 = map(changedate, time1str)
        time2 = [datetime.datetime.strptime(time_str, '%Y.%m.%d %H:%M:%S') for time_str in time1str]#起始时间格式转换
        time3 = [datetime.datetime.strptime(time_str, '%Y.%m.%d %H:%M:%S') for time_str in endtimestr]#结束时间格式转换
        #for x in time1:
        #    print(x)
        #print('time2')
        #for x in time2:
        #    print(x)
        time_start = []
        time_end = []
        #print('修改后')
        for t in time2:#调整时间差
            time_start.append(changetime(t, time_change))
        for t in time3:
            time_end.append(changetime(t, time_change))
        #for y in time_end:
        #    print(y)
        #将时间转换为字符串格式
        time_startstr = [datetime.datetime.strftime(y, '%Y.%m.%d %H:%M:%S') for y in time_start]
        time_endstr = [datetime.datetime.strftime(y, '%Y.%m.%d %H:%M:%S') for y in time_end]
        #写入起始时间列
        m = 1
        for t in time_startstr:
            wsheet.write(m,1,t)
            m = m + 1
        m = 1
        for t in time_endstr:
            wsheet.write(m,2,t)
            m = m+ 1
        #移除最后一行
        for nco in range(ncol):
            wsheet.write(r-1,nco,)
        os.remove(url)
        f1.save(url)
        print(name + '完成')

if __name__ == '__main__':

    excel_name = [ 'MBC 2 HD(H265).xls',  'MBC 4 HD(H265).xls', 'MBC Action HD(H265).xls',
                   'MBC Max HD.xls']
    #name = 'MBC 2 HD(H265).xls'
    for name in excel_name:
        url = './' + name
        file_exit = 0
        try:
            with open(url) as f:
                file_exit = 1
        except IOError:
            print('文件不存在')
        if file_exit == 1:
            f = xlrd.open_workbook(url, "rb",formatting_info=True)
            rsheet = f.sheet_by_index(0)#获取表格
            f1 = xlutils.copy.copy(f)#复制表格
            wsheet = f1.get_sheet(0)
            r = rsheet.nrows    #行数
            ncol = rsheet.ncols #列数
            #print(ncol)
            #获取预告名称
            program = []
            program = firstrow(rsheet,r)
            # for t in program:
            #    print(t)
            #print(id(program))
            #print(id(firstrow(rsheet,r)))

            if name in ['MBC 2 HD(H265).xls', 'MBC Action HD(H265).xls']:#时间+7
                deitexcle(rsheet,wsheet,r,ncol,7)
            elif name in ['MBC 4 HD(H265).xls','MBC Max HD.xls']:#时间+8
                deitexcle(rsheet,wsheet,r,ncol,8)
            else:
                os.remove(url)
                f1.save(url)
                print(name + '完成')
    input('按任意键退出')

