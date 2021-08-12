# !/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os
import datetime


def get_info(path):
    with open(path+'/not_transcode.txt') as f:
        lines = f.readlines()
    print('lines:{}'.format(lines))
    return lines


if __name__ == '__main__':
    path = os.getcwd()
    print(path)
    start_time = datetime.datetime.now()
    dir_list1 = os.listdir(path)
    print('dir_list1:{}'.format(dir_list1))
    dir_list1.remove('move_videos.py')
    dir_list1.remove('not_transcode.txt')
    print('dir_list1:{}'.format(dir_list1))
    folder_list = []
    for file in dir_list1:
        if '.' not in file:
            print('folder:{}'.format(file))
            dir_list1.remove(file)
            folder_list.append(file)
        else:
            print('file:{}'.format(file))
    print('dir_list1:{}'.format(dir_list1))
    print('folder_list:{}'.format(folder_list))
    ntrans_list = []
    for i in get_info(path):
        ntrans_list.append(i.strip())

    for nt_video in ntrans_list:
        if nt_video in dir_list1:
            folder_name = nt_video.split('.')[-1].upper()
            # print(folder_name)
            move_to = path + '/' + folder_name
            if folder_name not in folder_list:
                command1 = 'mkdir '+move_to
                a = subprocess.getstatusoutput(command1)
                # print('a:'.format(a))
            command2 = 'mv '+nt_video+' '+move_to
            print(command2)
            b = subprocess.getstatusoutput(command2)
            # print('b:'.format(b))