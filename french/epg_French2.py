# -*- coding=utf-8 -*-

import requests
import time
import datetime
import xlwt

from bs4 import BeautifulSoup

urls = ['http://www.programme-tv.net/programme/chaine/%s/programme-m6-boutique-co-238.html']
names = ['M6 Boutique(H265)']


def trans_format(time_string, from_format, to_format='%Y.%m.%d %H:%M:%S'):
    time_struct = time.strptime(time_string, from_format)
    times = time.strftime(to_format, time_struct)
    return times


def output_excel(items, channelname):
        if len(items) == 0:
            return
        workbook = xlwt.Workbook(encoding="utf-8", style_compression=2)
        sheet = workbook.add_sheet("epg", cell_overwrite_ok=True)
        head = ["预告名称", "开始时间", "结束时间", "系统录制文件保存天数", "是否允许系统录制", "TVOD计费方式", "TVOD计费单位", " ", "是否允许个人录制", "个人录制计费方式",
                "个人计费单位", "个人录制价格", "预告简介"]
        for i in range(len(head)):
            sheet.write(0, i, head[i], set_style("head"))


        index = 1
        for item in items:
            sheet.write(index, 0, item["name"], set_style("body"))
            sheet.write(index, 1, item["starttime"], set_style("body"))
            sheet.write(index, 2, item["endtime"], set_style("body"))
            sheet.write(index, 3, "3", set_style("body"))
            sheet.write(index, 4, "1", set_style("body"))
            sheet.write(index, 5, "0", set_style("body"))
            sheet.write(index, 6, "1", set_style("body"))
            sheet.write(index, 7, "0", set_style("body"))
            sheet.write(index, 8, "0", set_style("body"))
            sheet.write(index, 9, "0", set_style("body"))
            sheet.write(index, 10, "0", set_style("body"))
            sheet.write(index, 11, "0", set_style("body"))
            sheet.write(index, 12, item["desc"], set_style("body"))
            index += 1

        workbook.save(channelname + ".xls")


def set_style(t):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    if t == "head":
        font.name = "Time New Roman"
        font.height = 220
        font.bold = True
        font.color_index = 4
    elif t == "body":
        font.name = "Time New Roman"
        font.height = 220
        font.bold = False
        font.color_index = 4
    style.font = font
    return style


def get_epg(url):
    date_str = time.strftime("%Y-%m-%d")
    all_day_programs = []
    for i in range(7):
        epg_url = url % date_str
        c = requests.get(epg_url)
        html = c.content
        soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
        program_div_list = soup.select('div[class="broadcasts"]')[0]
        for program_div in program_div_list:
            if str(program_div).strip() == "":
                continue
            hour_span = program_div.select('span[class="hour"]')
            title_tag = program_div.select('.title')
            if len(hour_span) == 0 or len(title_tag) == 0:
                continue

            one_program = {}
            hour = hour_span[0].string
            
          #  strtime = trans_format(date_str + " " + hour, "%Y-%m-%d %H:%M:%S")
            date_time = datetime.datetime.strptime(date_str + " " + hour, "%Y-%m-%d %H:%M") + datetime.timedelta(hours=7)
            str_time  = date_time.strftime("%Y-%m-%d %H:%M")
            
            one_program['starttime'] = trans_format(str_time, "%Y-%m-%d %H:%M" )
            one_program['endtime'] = ""
            one_program['name'] = title_tag[0].string or "NoTitle"
            one_program['desc'] = title_tag[0].string or "NoTitle"

            all_day_programs.append(one_program)


  
        date_str_format = datetime.datetime.strptime(date_str, "%Y-%m-%d") + datetime.timedelta(days=1)
        date_str = date_str_format.strftime("%Y-%m-%d")
    for j in range(len(all_day_programs) - 1):
        all_day_programs[j]["endtime"] = all_day_programs[j + 1]["starttime"]

    return all_day_programs


for i in range(len(urls)):
    url = urls[i]
    name = names[i]
    print "Starting parse %s: %s" % (name, url)
    all_day_programs = get_epg(url)

    print "Starting write to excel...."
    output_excel(all_day_programs, name)

    print "Parsing %s finished!" %name
