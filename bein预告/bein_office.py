import requests
import datetime
import functools
from bs4 import BeautifulSoup
import os, time, re
import xlwt
import sys

sys.setrecursionlimit(200000)


""
''
"'" "'"

def html_to_excel(html, dtime):
    soup = BeautifulSoup(html, 'lxml')
    html = soup.find(name='div', attrs={'class': 'slider'}).prettify(formatter="html")
    results = re.findall('<li.*?data-img="(.*?)".*?onecontent.*?<p class="title">(.*?)</p>'
                         + '.*?<p class="format">(.*?)</p>'  # format
                         + '.*?<p class="time">(.*?)</p>'  # time
                         , html, re.S)
    prelog = ''
    count_row = 0
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet(dtime)

    for result in results:
        log = result[0].strip()
        *_, log = log.split('/')
        log, *_ = log.rpartition('.')
        title = result[1].strip()
        form = result[2].strip()
        time1, time2 = result[3].strip().split('-')
        time = time1.strip('&nbsp;') + '-' + time2.strip('&nbsp;')
        # 欧冠、英超、西甲 English Premier League
        flag = re.search('UEFA.*?Champions', form, re.IGNORECASE) or re.search('English.*?Premier.*?League', form,
                                                                               re.IGNORECASE) or re.search('La.*?Liga',
                                                                                                           form,
                                                                                                           re.IGNORECASE) or re.search(
            'Spanish.*?League', form, re.IGNORECASE) or re.search('Spanish.*Cup.*', form, re.IGNORECASE)
        if flag:
            if prelog != log:
                worksheet.write(count_row, 0, label='{}'.format(log))
                count_row += 4
                count_col = 1
            worksheet.write(count_row - 4, count_col, label='{}'.format(title))
            worksheet.write(count_row - 3, count_col, label='{}'.format(form))
            worksheet.write(count_row - 2, count_col, label='{}'.format(time))
            count_col += 1
            prelog = log
    if not os.path.exists(directory):
        os.mkdir(directory)
    workbook.save(str(directory) + '\官网{}.xls'.format(dtime))  # 表格名字


def logger(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        ret = fn(*args, **kwargs)
        delta = (datetime.datetime.now() - start).total_seconds()
        print('fun {} took {}s'.format(fn, delta))
        html_to_excel(ret, kwargs['dtime'])
        delta = (datetime.datetime.now() - start).total_seconds()
        print('total took {}s'.format(delta))

    return wrapper


@logger  # request_url = logger(request_url)
def request_url(url, *, dtime):
    l1 = ['cdate', 'offset', 'mins', 'category', 'serviceidentity', 'id']
    l2 = [dtime, '8', '00', 'sports', 'beinsports.com', '123']
    params = dict(zip(l1, l2))
    headers = dict({
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'})
    r = requests.get(url, params=params, headers=headers)
    return r.text


def bein_office(directory, url, nums):
    for i in range(nums):
        dtime = datetime.datetime.fromtimestamp((datetime.datetime.now().timestamp() + 86400 * i)).strftime('%Y-%m-%d')
        print(dtime)
        request_url(url, dtime=dtime)


directory = R'./'
url = 'https://epg.beinsports.com/utctime.php'
bein_office(directory, url, 5)