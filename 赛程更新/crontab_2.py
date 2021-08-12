# -*- coding: UTF-8 -*-

import xlrd
import datetime
from collections import defaultdict
import re


def source(x, y):
    print(x, y)
    lst = []
    for k, v in zip(x, y):
        if not v:
            continue
        dt, *_, notice = k.split()
        # print(v)
        tv, time_slot = v.split()
        tv = tv.lower()
        lst.append((dt, tv, notice, time_slot))
    # 排序
    fields = sorted(lst, key=lambda x: x[1], reverse=False)
    # 生成需要的几个台标
    keys = set(map(lambda x: x[1], lst))

    # 过滤每个台标对应的多个结果
    for key in keys:
        print('测试打印表格取得数据', sorted(filter(lambda x: x[1] == key, fields), key=lambda x: x[0]))
        yield list(filter(lambda x: x[1] == key, fields))


def crontab_source(time_diff, col3, d1, col1,
                   pre_time):  # time_diff, process_colume, tv_map_mark, date_colume, pre_time
    '''
    :param time_diff: 时差
    :param col3: 要完成crontab的列
    :param col1: 默认是第一列是时间
    :return: yield
    '''
    for x in source(col1, col3):
        yield from prome_same_tvid_list(d1, pre_time, time_diff, x)


def prome_same_tvid_list(d1, pre_time, time_diff, x):
    if len(x) > 1:
        print('--------------- len(x) > 1 -------------------')
        print(x)
        tvid = x[0][1]
        print(tvid)

        x_ = list(map(lambda x: (x[0], x[2], x[3]), x))
        lst = sorted(set(map(lambda x: (x[0]), x)), key=lambda x: x.split('-')[-1])
        # ['2018-12-23', '2018-12-22']

        # 为每个时间生成一个24小时的列表
        d2 = defaultdict(lambda: [0 for _ in range(24)])
        for x in lst:
            d2[x]
        # 将预告 < 起始时间, 就将起始时间的日期-1day. 预告01:00 起始 23：00,
        '''
        起始时间的日期，日期是由前面给定的日期确定
        因此，前面的日期一定是起始时间的日期
        '''
        # x_ = [('2018-12-22', '01:30', '22:30-03:55'), ('2018-12-22', '04:00', '03:30-06:30'), ('2018-12-22', '20:30', '20:00-23:00'), ('2018-12-22', '23:00', '23:00-01:30')]
        xx = []
        for ymd, notice, time in x_:
            start = time.split('-')[0]
            stop = time.split('-')[1]

            if not re.match('\d+:\d+', notice):
                notice = start

            print(start, notice, stop)

            if notice < start:
                # print(ymd, notice, start)
                dt = datetime.datetime.strptime(ymd, '%Y-%m-%d')
                d = datetime.timedelta(days=1)
                ymd = (dt - d).strftime('%Y-%m-%d')
                d2[ymd]
                xx.append((ymd, notice, time))
                continue
            xx.append((ymd, notice, time))

        # print(xx)  # 正确的时间
        # print(d2)  # 为正确的时间生成每天的标记

        # 遍历时间, 打标记, 都按整点取, start,会提前59分钟. stop会少59分钟. 在crontab中
        # [('2018-12-23', '01:30', '01:30-03:55'), ('2018-12-22', '04:00', '03:30-06:30'), ('2018-12-22', '20:30', '20:00-23:00'), ('2018-12-22', '23:00', '23:00-01:30')]

        #         2018-12-23 01:30-03:55
        #         2018-12-22 03:30-06:30
        #         2018-12-22 20:00-23:00
        #         2018-12-22 23:00-01:30
        # 3 6 start 3 stop 6 提前1小时, 延迟加2小时, stop 8; start 2 stop 8
        # 20 3 start 20 stop 3  start 19 stop 5

        for ymd, notice, time in xx:
            # 01:30-03:55
            regex = re.compile(':|-')
            start, _, stop, _ = regex.split(time)
            # print(ymd, start, stop)
            start = int(start)
            stop = int(stop)
            # print(start, notice, stop)
            d2[ymd][start] += 1
            # 判断结束
            '''
            结束时间的确定，日期由起始日期向后推的时间
            '''
            if stop < start:
                dt = datetime.datetime.strptime(ymd, '%Y-%m-%d')
                d = datetime.timedelta(days=1)
                ymd = (dt + d).strftime('%Y-%m-%d')
                d2[ymd]
            d2[ymd][stop] += 1

        # defaultdict(<function <lambda> at 0x0497A150>, {'2018-12-22': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2], '2018-12-23': [0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})
        print(d2)

        ymd_lst = sorted(list(map(lambda x: x[0], d2.items())))  # ['2018-12-22', '2018-12-23']
        print(ymd_lst)

        # rand4 = []
        # for i in ymd_lst:
        #     for v in d2.get(i):
        #         rand4.append(v)
        # print(rand4)
        total_lst = [v for i in ymd_lst for v in d2.get(i)]
        print(total_lst)
        flag = True
        stop = None
        prev = None
        for i, x in enumerate(total_lst):

            if flag:
                if int(x) == 1:
                    flag = False
                    if i > 23:  # 24时
                        index = i // 24
                        time = i - 24 * index
                    else:
                        index = 0
                        time = i  # 起始

                    print('flag 进入起始位置, 列表中的索引位置: %s' % i, "值: {}".format(x), "时间: {}".format(time))

                    # 2018-12-22 22:00
                    start = '{} {}'.format(ymd_lst[index], time)
                    print("北京起始 {}点".format(start))
                    dt = datetime.datetime.strptime(start, '%Y-%m-%d %H')
                    # 北京要-7小时, 为了提前录制-8小时
                    h1 = datetime.timedelta(hours=time_diff)
                    h2 = datetime.timedelta(hours=pre_time)
                    print(
                        '>>>>换算{}时差后的起始: {}点'.format(time_diff + pre_time, (dt - h1 - h2).strftime('%Y-%m-%d %H')))
                    if stop is not None:
                        print('开始判断本次起始和上次结束时间的关系-----------------------------------')
                        startdate = (lambda x: '{}-{}-{}'.format(x.year, x.month, x.day))(
                            datetime.datetime.strptime(start, '%Y-%m-%d %H') - h1 - h2)
                        stopdate = (lambda x: '{}-{}-{}'.format(x.year, x.month, x.day))(
                            datetime.datetime.strptime(stop, '%Y-%m-%d %H') - h1 + h2 + h2)
                        startdate = datetime.datetime.strptime(startdate, "%Y-%m-%d")
                        stopdate = datetime.datetime.strptime(stopdate, "%Y-%m-%d")

                        _a = startdate.strftime('%Y-%m-%d')
                        _b = stopdate.strftime('%Y-%m-%d')
                        if startdate == stopdate:
                            print('判断出 换算{}时差后 本次起始日期{} 和 上次结束日期{} 相等.'.format(time_diff, _a, _b))
                            tmpstart = (lambda x: x.hour)(
                                datetime.datetime.strptime(start, '%Y-%m-%d %H') - h1 - h2)  # 本次start时间
                            tmpstop = (lambda x: x.hour)(
                                datetime.datetime.strptime(stop, '%Y-%m-%d %H') - h1 + h2 + h2)  # 上次stop时间
                            if tmpstart < tmpstop:
                                print('判断出 换算{}时差后 本次起始时间{} 小于 上次结束时间{}, 跳过上次结束(同一天) .'.format(time_diff, tmpstart,
                                                                                               tmpstop))
                                continue
                            print('判断出 换算{}时差后 本次起始时间{} 大于 上次结束时间{}, 所以正常打印上次结束(同一天) .'.format(time_diff, tmpstart,
                                                                                               tmpstop))
                        elif startdate > stopdate:  # 本次大，应该显示上次的值
                            print('判断出 换算{}时差后 本次起始日期{} 大于 上次结束日期{} 所以正常打印上次结束(不同一天).'.format(time_diff, _a, _b))
                        elif startdate < stopdate:
                            print(
                                '判断出 换算{}时差后 本次起始日期{} 小于 上次结束日期{}, 跳过上次结束.'.format(time_diff, startdate, stopdate))
                            continue
                    if prev:
                        print(prev)
                        yield prev
                    current = (dt - h1 - h2).strftime(
                        '%M %H %d %m * monit ' + 'start' + ' %s' % (d1.get(tvid.lower())))
                    print(current)
                    yield current

                    continue
            #  {'2018-12-22': [0, 0, 0, 1, 0, 0, 1, 0
            if not flag:
                if int(x) == 1:
                    flag = True
                    if i > 23:  # 24时
                        stopindex = i // 24
                        stoptime = i - 24 * stopindex
                    else:
                        stopindex = 0
                        stoptime = i
                    print('not flag 表示进入结束位置, 列表中的索引位置: %s' % i, "值: {}".format(x), "时间: {}".format(stoptime))
                    # 2018-12-22 23:00
                    stop = '{} {}'.format(ymd_lst[stopindex], stoptime)
                    print("北京结束 {}点".format(stop))
                    dt = datetime.datetime.strptime(stop, '%Y-%m-%d %H')
                    # 北京要-7小时,,延后结束+2小时（1小时延迟，1小时是补偿整点）
                    h1 = datetime.timedelta(hours=time_diff)
                    h2 = datetime.timedelta(hours=2)
                    print('>>>>换算{}时差后的结束: {}点'.format(time_diff - 2, (dt - h1 + h2).strftime('%Y-%m-%d %H')))
                    prev = (dt - h1 + h2).strftime(
                        '%M %H %d %m * monit ' + 'stop' + ' %s' % (d1.get(tvid.lower())))
                    print('延迟打印结束, 在下一个起始时判断是否应该打印当前的结束. 如果起始时间小于当前结束, 不打印。如果大于就打印...\n')
        else:
            print(prev)
            yield prev
    else:  # == 1
        print('--------------- len(x) == 1 -------------------')
        print(x[0][1])
        notice = x[0][2]
        start = x[0][3].split('-')[0]
        second = x[0][3].split('-')[1]
        if not re.match('\d+:\d+', notice):
            notice = start
        print(start, notice, second)

        # 判断第一个时间的当前日期
        if start <= notice:  # 起始 <= 预告, 当前时间就是今天
            dt1 = x[0][0]
        else:  # start > notice, 减一天
            # 22:55 01:00
            # 2018-12-22
            a = x[0][0]
            b = datetime.datetime.strptime(a, '%Y-%m-%d')
            d = datetime.timedelta(days=1)
            dt1 = (b - d).strftime('%Y-%m-%d')

        print(dt1)
        # 2018-12-22-22:55
        dt = datetime.datetime.strptime(dt1 + '-' + start, '%Y-%m-%d-%H:%M')
        # 北京要-7小时, 为了提前录制-8小时
        h1 = datetime.timedelta(hours=time_diff)
        h2 = datetime.timedelta(hours=pre_time)
        tvid = d1.get(x[0][1].lower())
        print((dt - h1 - h2).strftime('%M %H %d %m * monit ' + 'start' + ' %s' % (tvid)))
        yield (dt - h1 - h2).strftime('%M %H %d %m * monit ' + 'start' + ' %s' % (tvid))

        # 判断第二个时间的当前日期
        if start <= second:
            dt2 = dt1
        else:  # second < start, 加一天
            # 22:55 01:00
            b = datetime.datetime.strptime(dt1, '%Y-%m-%d')
            d = datetime.timedelta(days=1)
            dt2 = (b + d).strftime('%Y-%m-%d')
        print(dt2)
        # 2018-12-23-01:00
        dt = datetime.datetime.strptime(dt2 + '-' + second, '%Y-%m-%d-%H:%M')
        # 北京要-7小时,延后结束+1小时
        h1 = datetime.timedelta(hours=time_diff)
        h2 = datetime.timedelta(hours=1)
        tvid = d1.get(x[0][1].lower())
        print((dt - h1 + h2).strftime('%M %H %d %m * monit ' + 'stop' + ' %s' % (tvid)))
        yield (dt - h1 + h2).strftime('%M %H %d %m * monit ' + 'stop' + ' %s' % (tvid))

def prome_same_tvid_list_espn(d1, pre_time, time_diff, x):
    if len(x) > 1:
        print('--------------- len(x) > 1 -------------------')
        print(x)
        tvid = x[0][1]
        print(tvid)

        x_ = list(map(lambda x: (x[0], x[2], x[3]), x))
        lst = sorted(set(map(lambda x: (x[0]), x)), key=lambda x: x.split('-')[-1])
        # ['2018-12-23', '2018-12-22']

        # 为每个时间生成一个24小时的列表
        d2 = defaultdict(lambda: [0 for _ in range(24)])
        for x in lst:
            d2[x]
        # 将预告 < 起始时间, 就将起始时间的日期-1day. 预告01:00 起始 23：00,
        '''
        起始时间的日期，日期是由前面给定的日期确定
        因此，前面的日期一定是起始时间的日期
        '''
        # x_ = [('2018-12-22', '01:30', '22:30-03:55'), ('2018-12-22', '04:00', '03:30-06:30'), ('2018-12-22', '20:30', '20:00-23:00'), ('2018-12-22', '23:00', '23:00-01:30')]
        xx = []
        for ymd, notice, time in x_:
            start = time.split('-')[0]
            stop = time.split('-')[1]

            if not re.match('\d+:\d+', notice):
                notice = start

            print(start, notice, stop)

            if notice < start:
                # print(ymd, notice, start)
                dt = datetime.datetime.strptime(ymd, '%Y-%m-%d')
                d = datetime.timedelta(days=1)
                ymd = (dt - d).strftime('%Y-%m-%d')
                d2[ymd]
                xx.append((ymd, notice, time))
                continue
            xx.append((ymd, notice, time))

        # print(xx)  # 正确的时间
        # print(d2)  # 为正确的时间生成每天的标记

        # 遍历时间, 打标记, 都按整点取, start,会提前59分钟. stop会少59分钟. 在crontab中
        # [('2018-12-23', '01:30', '01:30-03:55'), ('2018-12-22', '04:00', '03:30-06:30'), ('2018-12-22', '20:30', '20:00-23:00'), ('2018-12-22', '23:00', '23:00-01:30')]

        #         2018-12-23 01:30-03:55
        #         2018-12-22 03:30-06:30
        #         2018-12-22 20:00-23:00
        #         2018-12-22 23:00-01:30
        # 3 6 start 3 stop 6 提前1小时, 延迟加2小时, stop 8; start 2 stop 8
        # 20 3 start 20 stop 3  start 19 stop 5

        for ymd, notice, time in xx:
            # 01:30-03:55
            regex = re.compile(':|-')
            start, _, stop, _ = regex.split(time)
            # print(ymd, start, stop)
            start = int(start)
            stop = int(stop)
            # print(start, notice, stop)
            d2[ymd][start] += 1
            # 判断结束
            '''
            结束时间的确定，日期由起始日期向后推的时间
            '''
            if stop < start:
                dt = datetime.datetime.strptime(ymd, '%Y-%m-%d')
                d = datetime.timedelta(days=1)
                ymd = (dt + d).strftime('%Y-%m-%d')
                d2[ymd]
            d2[ymd][stop] += 1

        # defaultdict(<function <lambda> at 0x0497A150>, {'2018-12-22': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2], '2018-12-23': [0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})
        print(d2)

        ymd_lst = sorted(list(map(lambda x: x[0], d2.items())))  # ['2018-12-22', '2018-12-23']
        print(ymd_lst)

        # rand4 = []
        # for i in ymd_lst:
        #     for v in d2.get(i):
        #         rand4.append(v)
        # print(rand4)
        total_lst = [v for i in ymd_lst for v in d2.get(i)]
        print(total_lst)
        flag = True
        stop = None
        prev = None
        for i, x in enumerate(total_lst):

            if flag:
                if int(x) == 1:
                    flag = False
                    if i > 23:  # 24时
                        index = i // 24
                        time = i - 24 * index
                    else:
                        index = 0
                        time = i  # 起始

                    print('flag 进入起始位置, 列表中的索引位置: %s' % i, "值: {}".format(x), "时间: {}".format(time))

                    # 2018-12-22 22:00
                    start = '{} {}'.format(ymd_lst[index], time)
                    print("北京起始 {}点".format(start))
                    dt = datetime.datetime.strptime(start, '%Y-%m-%d %H')
                    # 北京要-7小时, 为了提前录制-8小时
                    h1 = datetime.timedelta(hours=time_diff)
                    h2 = datetime.timedelta(hours=pre_time)
                    print('ESPN')
                    print(
                        '>>>>换算{}时差后的起始: {}点'.format(time_diff + pre_time, (dt + h1 - h2).strftime('%Y-%m-%d %H')))
                    if stop is not None:
                        print('开始判断本次起始和上次结束时间的关系-----------------------------------')
                        startdate = (lambda x: '{}-{}-{}'.format(x.year, x.month, x.day))(
                            datetime.datetime.strptime(start, '%Y-%m-%d %H') + h1 - h2)
                        stopdate = (lambda x: '{}-{}-{}'.format(x.year, x.month, x.day))(
                            datetime.datetime.strptime(stop, '%Y-%m-%d %H') + h1 + h2 + h2)
                        startdate = datetime.datetime.strptime(startdate, "%Y-%m-%d")
                        stopdate = datetime.datetime.strptime(stopdate, "%Y-%m-%d")

                        _a = startdate.strftime('%Y-%m-%d')
                        _b = stopdate.strftime('%Y-%m-%d')
                        if startdate == stopdate:
                            print('判断出 换算{}时差后 本次起始日期{} 和 上次结束日期{} 相等.'.format(time_diff, _a, _b))
                            tmpstart = (lambda x: x.hour)(
                                datetime.datetime.strptime(start, '%Y-%m-%d %H') + h1 - h2)  # 本次start时间
                            tmpstop = (lambda x: x.hour)(
                                datetime.datetime.strptime(stop, '%Y-%m-%d %H') + h1 + h2 + h2)  # 上次stop时间
                            if tmpstart < tmpstop:
                                print('判断出 换算{}时差后 本次起始时间{} 小于 上次结束时间{}, 跳过上次结束(同一天) .'.format(time_diff, tmpstart,
                                                                                               tmpstop))
                                continue
                            print('判断出 换算{}时差后 本次起始时间{} 大于 上次结束时间{}, 所以正常打印上次结束(同一天) .'.format(time_diff, tmpstart,
                                                                                               tmpstop))
                        elif startdate > stopdate:  # 本次大，应该显示上次的值
                            print('判断出 换算{}时差后 本次起始日期{} 大于 上次结束日期{} 所以正常打印上次结束(不同一天).'.format(time_diff, _a, _b))
                        elif startdate < stopdate:
                            print(
                                '判断出 换算{}时差后 本次起始日期{} 小于 上次结束日期{}, 跳过上次结束.'.format(time_diff, startdate, stopdate))
                            continue
                    if prev:
                        print(prev)
                        yield prev
                    current = (dt + h1 - h2).strftime(
                        '%M %H %d %m * monit ' + 'start' + ' %s' % (d1.get(tvid.lower())))
                    print(current)
                    yield current

                    continue
            #  {'2018-12-22': [0, 0, 0, 1, 0, 0, 1, 0
            if not flag:
                if int(x) == 1:
                    flag = True
                    if i > 23:  # 24时
                        stopindex = i // 24
                        stoptime = i - 24 * stopindex
                    else:
                        stopindex = 0
                        stoptime = i
                    print('not flag 表示进入结束位置, 列表中的索引位置: %s' % i, "值: {}".format(x), "时间: {}".format(stoptime))
                    # 2018-12-22 23:00
                    stop = '{} {}'.format(ymd_lst[stopindex], stoptime)
                    print("北京结束 {}点".format(stop))
                    dt = datetime.datetime.strptime(stop, '%Y-%m-%d %H')
                    # 北京要-7小时,,延后结束+2小时（1小时延迟，1小时是补偿整点）
                    h1 = datetime.timedelta(hours=time_diff)
                    h2 = datetime.timedelta(hours=2)
                    print('>>>>换算{}时差后的结束: {}点'.format(time_diff - 2, (dt + h1 + h2).strftime('%Y-%m-%d %H')))
                    prev = (dt + h1 + h2).strftime(
                        '%M %H %d %m * monit ' + 'stop' + ' %s' % (d1.get(tvid.lower())))
                    print('延迟打印结束, 在下一个起始时判断是否应该打印当前的结束. 如果起始时间小于当前结束, 不打印。如果大于就打印...\n')
        else:
            print(prev)
            yield prev
    else:  # == 1
        print('--------------- len(x) == 1 -------------------')
        print(x[0][1])
        notice = x[0][2]
        start = x[0][3].split('-')[0]
        second = x[0][3].split('-')[1]
        if not re.match('\d+:\d+', notice):
            notice = start
        print(start, notice, second)

        # 判断第一个时间的当前日期
        if start <= notice:  # 起始 <= 预告, 当前时间就是今天
            dt1 = x[0][0]
        else:  # start > notice, 减一天
            # 22:55 01:00
            # 2018-12-22
            a = x[0][0]
            b = datetime.datetime.strptime(a, '%Y-%m-%d')
            d = datetime.timedelta(days=1)
            dt1 = (b - d).strftime('%Y-%m-%d')

        print(dt1)
        # 2018-12-22-22:55
        dt = datetime.datetime.strptime(dt1 + '-' + start, '%Y-%m-%d-%H:%M')
        # 北京要-7小时, 为了提前录制-8小时
        h1 = datetime.timedelta(hours=time_diff)
        h2 = datetime.timedelta(hours=pre_time)
        tvid = d1.get(x[0][1].lower())
        print((dt + h1 - h2).strftime('%M %H %d %m * monit ' + 'start' + ' %s' % (tvid)))
        yield (dt + h1 - h2).strftime('%M %H %d %m * monit ' + 'start' + ' %s' % (tvid))

        # 判断第二个时间的当前日期
        if start <= second:
            dt2 = dt1
        else:  # second < start, 加一天
            # 22:55 01:00
            b = datetime.datetime.strptime(dt1, '%Y-%m-%d')
            d = datetime.timedelta(days=1)
            dt2 = (b + d).strftime('%Y-%m-%d')
        print(dt2)
        # 2018-12-23-01:00
        dt = datetime.datetime.strptime(dt2 + '-' + second, '%Y-%m-%d-%H:%M')
        # 北京要-7小时,延后结束+1小时
        h1 = datetime.timedelta(hours=time_diff)
        h2 = datetime.timedelta(hours=1)
        tvid = d1.get(x[0][1].lower())
        print((dt + h1 + h2).strftime('%M %H %d %m * monit ' + 'stop' + ' %s' % (tvid)))
        yield (dt + h1 + h2).strftime('%M %H %d %m * monit ' + 'stop' + ' %s' % (tvid))



def read_excel(path):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    col1 = [i for i in table.col_values(0)]
    col3 = [i for i in table.col_values(2)]  # col3是AR
    col4 = []  # col4是ENG
    col5 = []

    try:
        col4 = [i for i in table.col_values(3)]
    except:
        pass

    try:
        col5 = [i for i in table.col_values(4)]
    except:
        pass

    print('read_excel')
    print('col1', col1)
    print('col3', col3)
    print('col4', col4)
    print('col5', col5)
    return col1, col3, col4, col5, table


def write_to_text(col3, col4, col5, write, write_espn):
    with open('crontab-142-155.txt', 'w+') as fb1:
        with open('crontab-253-31.txt', 'w+') as fb2:
            if col3:
                write(col3, fb1, fb2)
            if col4:
                write(col4, fb1, fb2)
            if col5:
                write_espn(col5, fb1, fb2)  # col5是POR


def espns(col5):
    print('处理字段5')
    # print(col5)
    fields = list(filter(lambda x: x != '', col5))
    col5 = [(field.split()[0], field.split()[2],  field.split()[1].split('-')[0], field.split()[1]) for field in fields]

    espn_keys = set(map(lambda x: x[1],col5))

    for espn_key in espn_keys:
        print('测试打印表格取得数据', sorted(filter(lambda x: x[1] == espn_key, col5), key=lambda x: x[0]))
        yield list(filter(lambda x: espn_key == x[1],col5)) # [('2019-08-24', 'bein1', '22:00', '21:55-00:00'), ('2019-08-25', 'bein1', '23:30', '23:25-01:30'), ('2019-08-25', 'bein1', '03:00', '02:55-05:00')])

def process_espn_source(espn_time_diff, col5, pre_time,espn_tv_map_mark):
    print('开始处理ESPN')
    print(espn_time_diff)
    print(col5)
    print(pre_time)

    for x in espns(col5):  # espn标识
        # pass # [('2019-09-01', 'ee', '12:15', '12:15-14:30')]
        print(espn_time_diff)
        yield from prome_same_tvid_list_espn(espn_tv_map_mark, pre_time, espn_time_diff, x)


def main(path, time_diff, tv_map_mark, pre_time, regex, espn_time_diff,espn_tv_map_mark):
    # 读取字段, col1, col3, col4, col5
    date_colume, col3, col4, col5, table = read_excel(path)
    print(date_colume, col3, col4, col5, table, 'main')

    # 传入不同的字段生成不同的crontab
    def write(process_colume, fb1, fb2):
        for x in crontab_source(time_diff, process_colume, tv_map_mark, date_colume, pre_time):
            fb1.write(x + '\n')
            x = regex.sub('TV420', x)  # 替换TV506为TV420
            fb2.write(x + '\n')
        fb1.write('\n')
        fb2.write('\n')

    def write_espn(col5, fb1, fb2):
        # process_espn_source(espn_time_diff, col5, pre_time,espn_tv_map_mark)
        for x in process_espn_source(espn_time_diff, col5, pre_time,espn_tv_map_mark):
            # print(x)
            # pass
            fb1.write(x + '\n')
            fb2.write(x + '\n')

    # 写crontab
    write_to_text(col3, col4, col5, write, write_espn)


if __name__ == "__main__":
    # 预编译
    regex = re.compile('TV506')

    # 解析字典
    tv_map_mark = {
        'bein1': 'TV5061',
        'bein2': 'TV5062',
        'bein3': 'TV5063',
        'bein4': 'TV5064',
        'bein5': 'TV5065',
        'bein6': 'TV5066',
        'bein7': 'TV5067',
        'bein8': 'TV5068',
        'bein9': 'TV4212',
        'bein10': 'TV4213',
        'bein11': 'TV4214',
        'bein12': 'TV4215',
        'bein13': 'TV4216',
    }

    espn_tv_map_mark = {
        'e': 'TV3141',  # Espn
        'e2': 'TV3205',  # ESPN 2 HD
        'eb': 'TV3233',  # ESPN Brasil
        'ee': 'TV3201',  # ESPN Extra
    }

    # crontab excel文件的位置
    path = R'E:\untitled3\赛程更新\crontab.xlsx'

    # time_diff时差
    time_diff = 7

    espn_time_diff = 5

    # 提前2个小时, 本应该提前一个小时, 但是因为bein官网时间和北京时间差距1小时.
    pre_time = 1

    main(path, time_diff, tv_map_mark, pre_time, regex, espn_time_diff,espn_tv_map_mark)
