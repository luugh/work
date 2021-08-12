#!/usr/bin/python
# conding=urf-8

import pymysql
import datetime
import xlutils


def selectglist(channel):
    channelname = "'" + channel + "'"
    print(channelname)
    '''
    sql = "SELECT * FROM gl_program_2017_08 WHERE prog_id = " + channelname + " AND cdn_record_time > '2017-08-12' AND cdn_record_time < '2017-08-19'"

    m = cursor.execute(sql)
   
    print("W34该节目" + channelname + "访问量为：", m)

    sql = "SELECT * FROM gl_program_2017_08 WHERE prog_id = " + channelname + " AND cdn_record_time > '2017-08-19' AND cdn_record_time < '2017-08-26'"
    m = cursor.execute(sql)
    print("W35该节目" + channelname + "访问量为：", m)

    sql = "SELECT * FROM gl_program_2017_08 WHERE prog_id = " + channelname + " AND cdn_record_time > '2017-08-26'"
    m = cursor.execute(sql)
    sql = "SELECT * FROM gl_program WHERE prog_id = " + channelname + " AND cdn_record_time < '2017-09-02'"
    n = cursor.execute(sql)
    print("W36该节目" + channelname + "访问量为：", m + n)
    '''
    sql = "SELECT * FROM gl_program WHERE prog_id = " + channelname + " AND cdn_record_time > '2017-09-02'"
    m = cursor.execute(sql)
    print("W36该节目" + channelname + "访问量为：", m)


if __name__ == '__main__':
    channels = ['TV8101','TV8167','TV8145','TV8144','TV8166','TV8150','TV8157',
                'TV8190','TV8194','TV8122','TV8199','TV8191','TV8195','TV8159',
                'TV8193','TV8196','TV8192','TV8154','TV8155','TV8142','TV8148',
                'TV8141','TV8152','TV8151','TV8175','TV8146','TV8172','TV8173',
                'TV8149','TV8143','TV8183','TV8178','TV8176','TV8177','TV8170',
                'TV8160','TV8197','TV8189']
    #print(channels[0])
    db = pymysql.connect('221.4.223.105', 'monitor', 'monitor2016', 'glist')
    cursor = db.cursor()
    for channel in channels:
        selectglist(channel)

    db.close()