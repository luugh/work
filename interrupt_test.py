#!/usr/bin/python
#! coding:utf-8

import os

if __name__ == '__main__':

    with open('/home/interrupttest/dir') as f:
        lines = f.readlines()

    alrecord = lines
    print(lines)
    now = os.system('ls /opt/starview/cdn/hls/logs > newlines')
    with open('newlines') as f:
        lines1 = f.readlines()
        for line in lines1[:-1]:
            if line in alrecord:
                pass
            else:
                command1 = 'grep -C 0 "stream recovery!" /opt/starview/cdn/hls/logs/'+line.strip('\n')+'>> intertupt.text'
                print(command1)
                os.system(command1)
                command2 ='echo ' +line.strip('\n')+' >> dir'
                os.system(command2)