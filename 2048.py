# coding=utf-8
#!/usr/bin/env python


from optparse import OptionParser
import sys
from subprocess import call
from b2.console2 import *


from random import randint


class GameArry(object):

    __board = None  # 这是一个一维数组可以模拟二维数组　或者更高维
    __cmd = ConsoleString()  # 终端字符串格式化　得到有色字体的利器
    __score = 0  # 得分
    __key = Control()  # 　获得终端按键

    def __init__(self, hard=4):
        self.__hard = hard
        self.reset()

    def reset(self):
        if not self.__hard:
            self.__hard = 4
        elif not (isinstance(self.__hard, int) and self.__hard >= 4 and self.__hard <= 8):
            self.__hard = 4
        self.__board = [0 for _ in range(self.__hard * self.__hard)]
        self.__score = 0
        self.__create_point(2)

    def __create_point(self, n=1):
        __create = 0
        while __create < n:
            __r = self.__random(0, len(self.__board) - 1)
            if self.__board[__r] != 0:
                continue
            self.__board[__r] = 2 if self.__random(0,100) < 90 else 4
            __create += 1

    def __move(self, left, right, step, fi):
        '''
        功能：
        整个数组的移动
        left 循环控制
        fi -> 转换坐标方程
        '''
        sign = False
        for rl in range(self.__hard):
        # 上移　或者　下移　时　rl == 列数
        # 左移　或者　右移　时　rl == 行数
            for i in range(left, right, step):
                for j in range(left - step, i, step):
                    __index = fi(i, self.__hard, rl)
                    __next = fi(j, self.__hard, rl)
                    if self.__board[__index] == 0:
                        continue
                    if self.__board[__index] == self.__board[__next] or self.__board[__next] == 0:
                        __cool = True
                        for k in range(j + step,  i, step):
                            if self.__board[fi(k, self.__hard, rl)] != 0:
                                __cool = False
                                break
                        if not __cool:
                            continue

                        self.__board[
                            __next] += self.__board[__index]
                        self.__score += self.__board[__index]
                        self.__board[__index] = 0
                        sign = True
        return sign

    def down(self):
        # index = row * array_len + rl => 行数　＊　数组长度（４＊　４）　 rl 列数 =等于要移动的坐标
        # row = [2 , 1 , 0]
        #
        return self.__move(self.__hard - 2,  -1,
                           -1, lambda x, y, z: x * y + z)

    def up(self):
        '''
        数组上移　，　对应的操作是 up
        '''
        # index = row * array_ len
        # row = [1 , 2, 3]
        return self.__move(1, self.__hard, 1, lambda x, y, z: x * y + z)

    def left(self):
        '''
        数组左移　对应LEFT 按键
        '''
        return self.__move(1, self.__hard, 1, lambda x, y, z:  z * y + x)

    def right(self):
        return self.__move(self.__hard - 2,  -1,
                           -1, lambda x, y, z:  z * y + x)

    def __random(self, min, max):
        return randint(min, max)

    def __pgame(self):

        ConsoleString.consle_clear()
        # print 'xxxxxxxxxxxxxx'
        # for i in range(self.__hard):
        #     print self.__board[i * self.__hard: (i + 1) * self.__hard]

        for i in range(self.__hard):
            self.__cmd.clear()
            consle = []
            for j in range(self.__hard):
                if self.__board[i * self.__hard + j] == 0:
                    consle.append('%4s' % ' ')
                else:
                    consle.append(
                        '%4s' % str(self.__board[i * self.__hard + j]))
            self.__cmd.red.default.append_string(''.join(consle))
            ConsoleString.consle_show(self.__cmd)
        ConsoleString.consle_show('')
        ConsoleString.consle_show('')
        self.__cmd.clear()
        self.__cmd.red.default.append_string('\t\t\tScore:').green.default.append_string('%6s' % self.__score)
        ConsoleString.consle_show(self.__cmd)

    def start(self):
        '''
        游戏主ｍａｉｎ方法
        游戏开始
        '''

        while self.__islive():
            self.__pgame()
            key = self.__key.getKey()
            if key:
                if getattr(self,  key.lower())():
                    self.__create_point()
        ConsoleString.consle_show('')
        self.__cmd.clear()
        self.__cmd.red.default.append_string('\t\t\tGAME OVER!!!!!!!!!')
        ConsoleString.consle_show(self.__cmd)



    def __islive(self):
        '''
        判断游戏是否可以继续
        判断是否有空格的存在
        判断是否有一个方块与左面相同（其实你在我的右面　等于我的左面的左面）
        判断是否有一个方块于上面一个方块相同
        '''
        for i in range(self.__hard):
            for j in range(self.__hard):
                if self.__board[i * self.__hard + j] == 0:
                    return True
                elif (i - 1) > 0 and self.__board[(i - 1) * self.__hard + j] == self.__board[i * self.__hard + j]:
                    return True
                elif (j - 1) > 0 and self.__board[i * self.__hard + j] == self.__board[i * self.__hard + j - 1]:
                    return True
        return False



if __name__ == '__main__':
    c = GameArry()
    c.start()
