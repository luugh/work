# !/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

"""
星号三角形问题
n为行数，输出等腰三角形
i从0开始，第i行星号数为2*i+1
第i行星号前空格数为n-i-1个
"""

def sanjiao():
    n = int(input('请输入行数：'))
    for i in range(n):
        for t in range(n - i-1):
            print(' ', end='')
        for t in range(2*i+1):
            print('*', end='')
        print()

# sanjiao()


'''
Craps赌博游戏
玩家摇两颗色子 如果第一次摇出7点或11点 玩家胜
如果摇出2点 3点 12点 庄家胜 其他情况游戏继续
玩家再次要色子 如果摇出7点 庄家胜
如果摇出第一次摇的点数 玩家胜
否则游戏继续 玩家继续摇色子
玩家进入游戏时有1000元的赌注 全部输光游戏结束
'''
from random import randint


def craps():
    money = 1000
    print('你的初始资金为：%d' % money)
    go_on = True
    while money > 0:
        T = True
        try:
            while T:
                wager = int(input('请输入你的赌注：'))
                if wager < 0:
                    print('投注资金必须为正数’')
                elif money - wager > 0:
                    print('投注资金不能大于已拥有的资金')
                else:
                    T = False
        except ValueError:
            print('！请输入正确的数字,默认投注为0！')
            wager = 0
        first = randint(1, 6)+randint(1, 6)
        print('你的点数为： %d' % first)
        if first == 7 or first == 11:
            print('玩家胜！')
            money += wager
            print('你的资金还有：%d' % money)
            go_on = False
        elif first == 3 or first == 2 or first == 12:
            print('庄家胜！')
            money -= wager
            print('你的资金还有：%d' % money)
            go_on = False
        else:
            print('本轮无人胜出!')
            go_on = True
        while go_on:
            dice_points = randint(1, 6)+randint(1, 6)
            print('你的点数为：%d' % dice_points)
            if dice_points == 7:
                print('庄家胜！')
                money -= wager
                print('你的资金还有：%d' % money)
                go_on = False
            elif dice_points == first:
                print('玩家胜！')
                money += wager
                print('你的资金还有：%d' % money)
                go_on = False



# craps()

'''
输出斐波那契数列的前20个数
1 1 2 3 5 8 13 21 ...
从第三位开始，每位数字为前两位的和
'''


def feibona():
    list1 = [1, 1]

    for i in range(2, 20):
        list1.append(list1[i-1] + list1[i-2])
    print(list1)


def feibona1():
    a = 1
    b = 0
    for i in range(20):
        (a, b) = (b, a+b)
        print(b)

# feibona()
# feibona1()
'''
猜数字游戏
计算机出一个1~100之间的随机数由人来猜
计算机根据人猜的数字分别给出提示大一点/小一点/猜对了
'''

from random import randint


def guess():
    num = randint(1, 100)
    # print(num)
    n = 0
    while True:
        n += 1
        guess_num = int(input('请输入你猜测的数字(1-100)：'))
        if guess_num < num:
            print('你猜的数字小啦！')
        elif guess_num > num:
            print('你猜的数字大啦！')
        else:
            print('你猜对啦！')
            break
    print('你总共猜了 %d 次' % n)

# guess()


'''
找出100~999之间的所有水仙花数
水仙花数是各位立方和等于这个数本身的数
如: 153 = 1**3 + 5**3 + 3**3
//表示正数除法，结果只保留整数 
'''


def shuixian():
    for i in range(100, 1000):
        low = i % 10
        mid = i // 10 % 10
        hig = i // 100 % 10
        if low**3+mid**3+hig**3 == i:
            print(i)

# shuixian()

'''
判断输入的正整数是不是回文数
回文数是指将一个正整数从左往右排列和从右往左排列值一样的数
'''


def huiwen():
    num = int(input('请输入一个正整数：'))
    temp = num
    num1 = 0
    while temp:
        num1 *= 10
        num1 += temp % 10
        temp //= 10
    print(num)
    print(num1)
    if num1 == num:
        print('%d 是回文数' % num)
    else:
        print('%d 不是回文数' % num)

# huiwen()

'''
找出1~9999之间的所有完美数
完美数是除自身外其他所有因子的和正好等于这个数本身的数
例如: 6 = 1 + 2 + 3, 28 = 1 + 2 + 4 + 7 + 14
'''
from math import sqrt
import time

def wanmei():
    for n in range(2, 10000):
        num = 0
        # print('%d' % n)
        for i in range(2, n):
            if n % i == 0:
                num = num + i
        # print('%d' % num)
        if num + 1 == n:
            print('%d 是完美数' % n)


def wanmei1():
    for num in range(1, 10000):
        sum = 0
        for factor in range(1, int(sqrt(num)) + 1):
            if num % factor == 0:
                sum += factor
                if factor > 1 and num / factor != factor:
                    sum += num / factor
        if sum == num and num != 1:
            print(num)

#
# start1 = time.perf_counter()
# wanmei()
# end1 = time.perf_counter()
# start2 = time.perf_counter()
# wanmei1()
# end2 = time.perf_counter()
# time1 = end1-start1
# time2 = end2-start2
# print(time1)
# print(time2)

'''
输出2~99之间的素数
质数又称素数。一个大于1的自然数，除了1和它自身外，不能被其他自然数整除的数叫做质数；否则称为合数
'''


def sushu():
    for i in range(2, 100):
        # num = 0
        is_prime = True
        for n in range(2, int(sqrt(i))+1):
            if i % n == 0:
                is_prime = False
                break
                # num += 1
        # if num == 0:
        #     print(i)

        if is_prime:
            print(i)
# sushu()

'''
输出乘法口诀表(九九表)
'''


def shenfa():
    for x in range(1, 10):
        for y in range(1, x+1):
            print('%d x %d = %d' % (x, y, x*y), end='\t')
        print()

shenfa()

'''
输入M和N计算C(M,N)
'''


def cal():
    m = int(input('m = '))
    n = int(input('n = '))
