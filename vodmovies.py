#!/usr/bin/python
#coding:utf-8

import requests
import json
import os
import multiprocessing
import logging
import xlsxwriter
import xlwt

'''
def get_link():
    getlist = requests.get("http://38.91.107.246:8900/webProgram/getList?cid=2311")
    getlist_str = getlist.text
    getlist_dict = json.loads(getlist_str)
    #获取list列表
    list = getlist_dict['list']

    movies = {}
    for i in list:
        detailurl = i['detailUrl']
        get_detailurl = requests.get(detailurl)
        detail = json.loads(get_detailurl.text)

        terminalurl = detail['terminalStateUrl']
        getterminal = requests.get(terminalurl)
        playurl = json.loads(getterminal.text)['urlobj'][0]['playUrl']

        movies[i['name']] = playurl
    print(movies)
    print(len(movies))
'''

def get_links():
    get_flimeshd = requests.get('http://4535.mine.nu/panel/out/filmeshd.php?token=YldGNGRIWT0=')
    #去掉最左最右的空格
    flimeshd_list = json.loads(get_flimeshd.text.lstrip('(').rstrip(';').rstrip(')'))
    #print(flimeshd_list)
    #print(len(flimeshd_list))
    name_id = {}
    for i in flimeshd_list:
        name_id[i['nome']] = i['id']

    names = name_id.keys()
    name_link = {}
    print('正在获取下载link')
    for n in names:
        try:
            #print('http://4535.mine.nu/panel/out/filmeshd.php?token=YldGNGRIWT0=&mov_id=' + name_id[n])
            re = requests.get('http://4535.mine.nu/panel/out/filmeshd.php?token=YldGNGRIWT0=&mov_id=' + name_id[n])
            #print(re.text.lstrip('(').rstrip(';').rstrip(')'))
            # print(type(re.text.lstrip('(').rstrip(';').rstrip(')')))
            re_list = json.loads(re.text.lstrip('(').rstrip(';').rstrip(')'))

            playurl = re_list[0]['url']
            print(n + ' ' + playurl)
            name_link[n] = playurl
        except Exception as err:
            logging.exception(err)
            #print('获取' + n + ' 节目link失败')
            os.system('echo ' + n + 'http://4535.mine.nu/panel/out/filmeshd.php?token=YldGNGRIWT0=&mov_id=' + name_id[n] + ' >> fail_download')



    print('获取下载link成功')
    #print(name_link)
    print(len(name_link))
    return name_link

def curldownload(name, link):
    print('star download '+name)
    os.system('curl ' + link + ' -s -R 3 -o ' + name + '.mp4')
    print('download ' + name + 'completed')

def request_download(name, link):
    print('start download ' + name)
    try:
        dest_resp = requests.get(link)
        #视频是二进制数据流，content为获取二进制流的方法
        data = dest_resp.content
        #保存数据路径及文件
        path = './' + name + '.mp4'
        f = open(path, 'wb')
        f.write(data)
        f.close()
        os.system('echo "' + name + '" >> completed_movies')
        print('download [' + name + '] completed')
    except Exception as err:
        logging.exception(err)
        os.system('echo "' + name + ' ' + link +'" >> fail_download')
        print('download ['+name+'] failed')


def completed_movies():
    line =[]
    if os.path.exists('ompleted_movies'):
        with open('completed_movies') as f:
            line = f.readline()
    return line

if __name__ == "__main__":

    name_link = get_links()
    names = name_link.keys()


    '''
    #3个进程
    pool = multiprocessing.Pool(processes=1)
    names = name_link.keys()
    downed_name = completed_movies()
    if len(downed_name):
        for n in downed_name:
            if n in names:
                names.remove(n)

    for i in names:
        pool.apply_async(request_download, (i, name_link[i]))

    pool.close()
    pool.join()
    print('完成下载')
    
    '''