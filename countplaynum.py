#! /usr/bin/python
# -*- coding:utf-8 -*-

def getchannels():
    channels = {}
    with open('Spanish.txt', 'rb') as f:
        while 1:
            line = f.readline()
            print(line)
            print(line.split())
            if not line:
                continue
            channels[line.split()[0]] = line.split()[1]
    print(channels)
    return channels

if __name__ == '__main__':
     channels = getchannels()
     print(channels)