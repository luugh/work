# -*- coding:utf-8 -*-
import xlutils
import sys
import xlrd
import importlib
importlib.reload(sys);


def getncol_name(rsheet,row,ncol):  #表,行,列数
    num = []
    for i in range(1,row):
        num.append(rsheet.cell_value(i,2))
    return num


def getncol_cpcode(rsheet,row,ncol):  #表,行,列数
    num = []
    for i in range(1,row):
        num.append(rsheet.cell_value(i,1))
    return num


def geturl(rsheet,row,ncol):
    num = []
    for i in range(1, row):
        num.append(rsheet.cell_value(i,3))
    return num


if __name__ == '__main__':

    url = './Channel.xlsx'
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
        # print(ncol)
        # print(row)
        cpcode = []
        name = []
        srcurl = []
        name = getncol_name(rsheet,row,2)                            #获取第三列节目名称
        # print(name)
        cpcode = getncol_cpcode(rsheet,row,1)
        srcurl = geturl(rsheet,row,3)                               #获取第四列节目源url
        f1=open("./vlclist.xspf","w")
        f1.truncate()                                                #empty file
        f1.close()
        f1=open('./vlclist.xspf','a')
        f1.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f1.write(
        '<playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">\n')
        f1.write('	<title>Playlist</title>\n')
        f1.write('	<trackList>\n')
        n = 0
        for x in name:
            print(x)
            print(name[n])
            f1.write('		<track>\n')
            f1.write('			<location>' + srcurl[n] + '</location>\n')
            f1.write('           <title>'+name[n]+'-'+cpcode[n].replace('&', '_')+'</title>\n')
            # f1.write('           <title>' + name[n] + '"' + cpcode[n] + '"</title>\n')
            # f1.write('           <title>' + name[n] + '</title>\n')
            f1.write('			<extension application="http://www.videolan.org/vlc/playlist/0">\n')
            f1.write('				<vlc:id>'+str(n)+'</vlc:id>\n')
            f1.write('				<vlc:option>network-caching=1000</vlc:option>\n')
            f1.write('			</extension>\n')
            f1.write('		</track>\n')
            n = n + 1
        f1.write('	</trackList>\n')
        f1.write('	<extension application="http://www.videolan.org/vlc/playlist/0">\n')
        for i in range(0,n):
            f1.write('			<vlc:item tid="'+str(i)+'"/>\n')
        f1.write('	</extension>\n')
        f1.write('</playlist>\n')
        f1.close
        print('vlclist write complete')

