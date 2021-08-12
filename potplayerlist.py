#-*- coding=utf8 -*-

import xlrd
import sys

def getncol(rsheet,row,ncol):  #表,行,列数
    num = []
    for i in range(1,row):
        num.append(rsheet.cell_value(i,2))
    return num

def geturl(rsheet,row,ncol):
    num = []
    for i in range(1, row):
        num.append(rsheet.cell_value(i,3))
    return num


if __name__ == '__main__':

    url = sys.argv[1]
    file_exit = 0
    try:
        with open(url) as f:
            file_exit = 1
    except IOError:
        print('文件不存在')
    if file_exit == 1:
        f = xlrd.open_workbook(url,"rb")
        rsheet = f.sheet_by_index(0)                            #获取表格
        ncol = rsheet.ncols                                     #获取列数
        row  = rsheet.nrows                                     #获取行数
        #print(ncol)
        #print(row)
        name = []
        srcurl = []
        name = getncol(rsheet,row,2)                            #获取第3列唯一标识
        srcurl = geturl(rsheet,row,3)                           #获取第四列节目源url
        f1=open("./potplayerlist.dpl","w")
        f1.truncate();                                          #empty file
        f1.close()
        f1=open('./potplayerlist.dpl','a')
        f1.write('DAUMPLAYLIST\n')
        f1.write('playname=potplayerlist\n')
        f1.write('topindex='+str(ncol)+'\n')
        n = 0
        for x in name:
            f1.write(str(n+1)+'*file*'+srcurl[n]+'\n')
            f1.write(str(n+1)+'*title*'+name[n]+'--'+srcurl[n]+'\n')
            f1.write(str(n+1)+'*played*0'+'\n')
            n= n+1
        f1.close
        print('potplayerlist write complete')

