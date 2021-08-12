#encoding:UTF-8
import urllib.request
import datetime
from bs4 import BeautifulSoup
import xlrd
import xlwt
'''
today = datetime.date.today()
#print(endday)
#for循环获取日期
for i in range (0,7):
    targetday = today + datetime.timedelta(days = i)
    targetday_str = str(targetday)
    #print(targetday_str)

url = "http://epg.beinsports.com/utctime.php?cdate="+today+"&offset=+8&mins=00&category=sports&id=123"
'''
url = "http://www.foxplaybrasil.com.br/listings/2017-01-20"
data = urllib.request.urlopen(url).read()
#print(type(data))
#ata = data.decode()
#rint(type(data))
data_str = data.decode()
soup = BeautifulSoup(data_str,"html.parser")
#print(soup.prettify())
#print(soup)

sc=('row fox fox foxhd series',"row fox-hd fox foxhd series")
#print(sc[0])
Fox_name = []
for sd in sc:
    print(sd)
    biaoqian = soup.find('div',class_ = sd)
    #print(biaoqian)
    print('\n')
    program_time = []
    program_name = []
    program_name =biaoqian.find_all('h2')#提取h2标签
    program_time =biaoqian.find_all('h4')#提取h4标签
    print(program_name)
    print(program_time)
    if sd == 'row fox-hd fox foxhd series':
        program_name1 = []
        time_am = []        #开始时间
        time_pm = []        #结束时间
        #去除名字中的标签
        #program_name1 = [i.string for i in program_name ]
        for i in program_name:
            program_name1.append(i.string)
        print (program_name1)
        #处理时间
        timestring = "2107-01-27"
        program_time1 = [i.string for i in program_time]
        print(program_time1)
        tiemstr = timestring.replace('-','.')
        for t in program_time1:
            time_am.append(tiemstr+' '+t[0:5]+':00')
            time_pm.append(tiemstr+' '+t[-6:-1]+':00')
        print (time_am)
        print (time_pm)


def creat_excel(name1,time_start,time_end,excel_name):
    #获取模版表格中的第一行
   # model = xlrd.open_ex('./模版.xls')
    f =xlwt.Workbook(name1)
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    title = ['预告名称','开始时间','结束时间','系统录制文件保存天数','是否允许系统录制','TVOD计费方式','TVOD计费单位',' ','是否允许个人录制',
             '个人录制计费方式','个人计费单位','个人录制价格','预告简介']
    n = 0
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
        sheet1.write(1+n,3,'3')         #系统录制文件保存天数
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

creat_excel(program_name1,time_am,time_pm,'FOX')




'''
        for i in program_name1:
            Fox_name[m+1] = Fox_name[m] + i
'''
