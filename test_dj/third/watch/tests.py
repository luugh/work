from django.test import TestCase

# Create your tests here.

import queue
import time
import multiprocessing


def test(i, q):
    for m in range(2):
        time.sleep(10)
        q.put(m)
    q.put('test')
    print(i)


if __name__ == '__main__':
    q = multiprocessing.Manager().Queue()
    pool = multiprocessing.Pool(2)

    for i in range(1, 2):
        pool.apply_async(test, args=(i, q))
    pool.close()
    pool.join()
    print('q.qsize:')
    print(q.qsize())
    while not q.empty():
        print(q.get())
