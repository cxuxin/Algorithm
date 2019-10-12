#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : CXX
# @Time    : 2019/9/17
# @File    : test.py
# @Software: PyCharm
# @Project : Test
# @Desc    : 梅森旋转算法生成(0,1)随机数 并生成符合高斯分布随机数
import numpy as np
import matplotlib.pyplot as plt


class MersenneTwister:
    __n = 624
    __m = 397
    __a = 0x9908b0df
    __b = 0x9d2c5680
    __c = 0xefc60000
    __kInitOperand = 0x6c078965
    __kMaxBits = 0xffffffff
    __kUpperBits = 0x80000000
    __kLowerBits = 0x7fffffff

    def __init__(self, seed=0):
        self.__register = [0] * self.__n
        self.__state = 0

        self.__register[0] = seed
        for i in range(1, self.__n):
            prev = self.__register[i - 1]
            temp = self.__kInitOperand * (prev ^ (prev >> 30)) + i
            self.__register[i] = temp & self.__kMaxBits

    def __twister(self):
        for i in range(self.__n):
            y = (self.__register[i] & self.__kUpperBits) + \
                    (self.__register[(i + 1) % self.__n] & self.__kLowerBits)
            self.__register[i] = self.__register[(i + self.__m) % self.__n] ^ (y >> 1)
            if y % 2:
                self.__register[i] ^= self.__a
        return None

    def __temper(self):
        if self.__state == 0:
            self.__twister()

        y = self.__register[self.__state]
        y = y ^ (y >> 11)
        y = y ^ (y << 7) & self.__b
        y = y ^ (y << 15) & self.__c
        y = y ^ (y >> 18)

        self.__state = (self.__state + 1) % self.__n

        return y

    def __call__(self):
        return self.__temper()

    # def load_register(self, register):
    #     self.__state = 0
    #     self.__register = register


#  高斯分布概率密度函数
def gauss(x, mu=0, sigma=1):
    return (1 / np.sqrt(2 * np.pi) * sigma) * np.exp(-(np.power((x-mu), 2))/(2 * np.power(sigma, 2)))


if __name__ == "__main__":
    mt = MersenneTwister(0)
    sample = []
    sample_gauss = []
    size = 100000
    for i in range(size):
        t = mt()
        number = t/(2 ** 32 - 1)
        sample.append(number)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel('Values')  # 绘制x轴
    plt.ylabel('Numbers')  # 绘制y轴

    # 画随机数分布
    # plt.hist(sample, bins=100)
    # plt.title('梅森旋转算法得到[0,1]均匀分布随机数')
    # plt.show()

    # 画高斯分布
    for i in range(0, len(sample), 2):
        sample_gauss.append(np.sqrt(-2 * np.log(sample[i])) * np.cos(2 * np.pi * sample[i + 1]))
        sample_gauss.append(np.sqrt(-2 * np.log(sample[i])) * np.sin(2 * np.pi * sample[i + 1]))
    n, bins, patches = plt.hist(sample_gauss, 100)
    plt.plot(bins, gauss(bins) * max(n) * np.sqrt(2 * np.pi), 'r--')
    # plt.title(r'Histogram : $\mu=0$,$\sigma=1$')  # 中文标题 u'xxx'
    plt.title(u'（0，1）均匀分布生成高斯分布随机数')  # 中文标题 u'xxx'
    plt.show()
    print(2**32)