import re
from pyquery import PyQuery as pq
import requests
import datetime
import xlwt, os

# 英超
eng_premier = {
    '比尔森胜利': 'Viktoria Plzen',
    '莫斯科中央陆军': 'CSKA Moscow',
    '伯恩茅斯': 'A.F.C. Bournemouth',
    '哈德斯菲尔德': 'Huddersfield Town',
    '布莱顿': 'Brighton & Hove Albion F.C.',
    '水晶宫': 'Crystal Palace',
    '西汉姆联': 'West Ham United Football',
    '卡迪夫城': 'Cardiff City Football',
    '沃特福德': 'Watford Football',
    '曼城': 'Manchester City',
    '伯恩利': 'Burnley',
    '利物浦': 'Liverpool',
    '富勒姆': 'Fulham F.C.',
    '莱斯特城': 'Leicester City',
    '狼队': 'Wolverhampton Wanderers',
    '切尔西': 'Chelsea',
    '埃弗顿': 'Everton F.C.',
    '纽卡斯尔': 'Newcastle United',
    '曼联': 'Manchester United',
    '阿森纳': 'Arsenal',
    '热刺': 'Tottenham Hotspur Football',
    '南安普顿': 'Southampton',
    '卡迪夫': 'Cardiff City',
    '加拉塔萨雷': 'Galatasaray',
    '波尔图': 'FC Porto',
    '贝尔格莱德红星': 'Crvena Zvezda',
    '巴黎圣日耳曼': 'Paris Saint-Germain',
    "诺维奇": "Norwich City",
    "谢菲尔德联": "Sheffield United",
    "阿斯顿维拉": "Aston Villa"
}

# 欧冠
uefa_champ = {
    '马德里竞技': 'Atlético de Madrid',
    '摩纳哥': 'Monaco',
    '莫斯科火车头足球俱乐部': 'Lokomotiv Moscow',
    '加拉塔雷萨': 'Galatasaray',
    '那不勒斯': 'Napoli',
    '贝格莱德红星': 'Crvena Zvezda',
    '埃因霍温': 'PSV Eindhoven',
    '巴塞罗那': 'Barcelona',
    'Germain': 'Liverpool',
    '波尓图': 'FC Porto',
    '沙尔克': 'FC Schalke 04',
    '多特蒙德': 'Borussia Dortmund',
    '布鲁日': 'Club Brugge',
    '热刺': 'Tottenham Hotspur',
    '国际米兰': 'Internazionale',
    '雅典AEK': 'AEK Athens',
    '阿贾克斯': 'Ajax',
    '莫斯科中央': 'CSKA Moscow',
    '比尔森': 'Viktoria Plzen',
    '拜仁慕尼黑': 'FC Bayern München',
    '本菲卡': 'Benfica',
    '里昂': 'Lyon',
    '曼城': 'Manchester City',
    '霍芬海姆': 'TSG 1899 Hoffenheim',
    '顿涅茨克矿工': 'Shakhtar Donetsk',
    '罗马': 'Roma',
    '皇家马德里': 'Real Madrid',
    '尤文图斯': 'Juventus',
    '瓦伦西亚': 'Valencia CF',
    '曼联': 'Manchester United',
    '伯尔尼年轻人': 'Young Boys',
    '巴黎圣日耳曼': 'Paris Saint German',
    '波尔图': 'Porto',
    "利物浦": 'Liverpool',
}

# 西甲
spanish_la = {
    '巴拉多利德': 'Real Valladolid',
    '莱万特': 'Levante',
    '毕尔巴鄂': 'Athletic Bilbao',
    '巴列卡诺': 'Rayo Vallecano de Madrid',
    '埃瓦尔': 'Sociedad Deportiva Eibar',
    '塞尔塔': 'Celta Vigo',
    '韦斯卡': 'SD Huesca',
    '莱加内斯': 'Club Deportivo Leganés',
    '赫塔菲': 'Getafe',
    '西班牙人': 'Espanyol',
    '皇家马德里': 'Real Madrid',
    '瓦伦西亚': 'Valencia Club de Fútbol',
    '皇家贝蒂斯': 'Real Betis',
    '皇家社会': 'Real Sociedad',
    '赫罗纳': 'Girona',
    '马德里竞技': 'Atlético Madrid',
    '巴塞罗那': 'Barcelona',
    '比利亚雷亚尔': 'Villarreal',
    '阿拉维斯': 'Deportivo Alavés',
    '塞维利亚': 'Sevilla',
    '毕尔巴鄂竞技': 'Athletic Bilbao',
    '维戈塞尔塔': 'Celta Vigo'
}

mapd = {'英超': eng_premier, '欧冠': uefa_champ, '西甲': spanish_la}


def get_dt(doc):
    y = datetime.datetime.now().year
    m = doc('li.on a h2').text()[:2]
    w = doc('li.on a h2').text()[-2:]
    d = doc('li.on a h3').text()
    dt = '{}-{}-{}'.format(y, m, d)
    dt = datetime.datetime.strptime(dt, '%Y-%m-%d').strftime('%Y-%m-%d')
    return dt, w


def logger(fn):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        fn(*args, **kwargs)
        delta = (datetime.datetime.now() - start).total_seconds()
        print('func {} took {}s'.format(fn, delta))

    return wrapper


@logger
def info(url):
    r = requests.get(url)
    doc = pq(r.text)
    dt, w = get_dt(doc)
    lst1 = [i.text() for i in doc('div.leftList2').items()]
    tds = doc('div.leftList4')
    length = len(tds)
    tds = list(tds.items())
    workbook = xlwt.Workbook(encoding='ascii')
    flag = False
    for i in range(length):
        if lst1[i] not in ['欧冠', '英超', '西甲']:
            continue
        flag = True
        print(lst1[i])
        tmpd = mapd.get(lst1[i])
        shet = 'shet%s' % i
        shet = workbook.add_sheet(lst1[i])
        #         print(shet,lst1[i])
        results = re.findall('<td>(.*?)</td>.*?' +  # 轮次
                             '<td>(.*?)</td>.*?' +  # 时间
                             '<td>.*?<span class="c1">.*?>(.*?)</a>' +  # 第一组
                             '.*?<span class="c2">.*?><a.*?>(.*?)</a>' +  # 第二组
                             '.*?<td>.*?</td>.*?'  # XXXX
                             , tds[i].html(), re.S)
        count_row = 0
        for rounds, time, c1, c2, in results:
            time = time.strip()
            print("{1} {2} {3}    {4}-{5} ".format(rounds, dt, w, time, c1, c2))
            shet.write(count_row, 0, '{} {} {}'.format(dt, w, time))
            shet.write(count_row, 1, '{}-{}'.format(c1, c2))
            shet.write(count_row + 1, 1, '{} vs {}'.format(tmpd.get(c1, 'None'), tmpd.get(c2, 'None')))

            count_row += 2
    if not os.path.exists(directory):
        os.mkdir(directory)
    if flag:
        workbook.save(str(directory) + '\网易{}.xls'.format(dt))  # 表格名字


def bein_wangeyi(directory, nums):
    dt = datetime.datetime.now()
    for i in range(nums):
        newdt = dt + datetime.timedelta(days=i)
        newdt = newdt.strftime('%Y%m%d')
        url = 'http://goal.sports.163.com/schedule/%s.html' % (newdt,)
        info(url)


directory = R'./bein'
bein_wangeyi(directory, 5)