#!/usr/bin/env python3
# coding:utf-8

from multiprocessing.dummy import Pool as ThreadPool
import os


def curl(url):
    os.system(url)


url = ['curl http://50.7.34.3:80/TV3187@720 -o /dev/null',
       'curl http://50.7.34.3:80/TVTV3187@720 -o /dev/null']

while len(url) != 100:
    url.append('curl http://50.7.34.3:80/TVTV3187@720 -o /dev/null')
print(len(url))

pool = ThreadPool(100)
results = pool.map(curl, url)
pool.cloes()
pool.join()


