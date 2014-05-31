# coding=utf-8
#!/usr/bin/env python


from optparse import OptionParser
import sys
from subprocess import call


class ConsleString(object):

    '''
    终端颜色字体输出
    主要运用方式为
    cmd = ConsleString()
    cmd.red.black.append_string('hello word!')
    ConsleString.consle_show(cmd)
    但是每写一行要清空字符串的ｂｕｆｆｅｒ
    cmd.clear()
    ConsleString.consle_clear() #清除终端 clear 
    原理 : echo -e 
    特殊字符的颜色字体
    '''
    __strbuffer = []  # 字符串储存　
    __fore_color = False
    __append = False

    def append_string(self, value):
        if self.__strbuffer and not self.__fore_color:
            if self.__strbuffer[len(self.__strbuffer) - 1] != '1m' and self.__strbuffer[len(self.__strbuffer) - 1] != '0m':
                self.__strbuffer.append('1m')
            self.__append = False
            self.__strbuffer.append(value)
        return self

    def clear(self):
        if self.__strbuffer and len(self.__strbuffer) > 0:
            del self.__strbuffer[:]
            self.__append = False
            self.__fore_color = False

    def __getattr__(self, key):
        if not self.__strbuffer:
            self.__strbuffer = list()
        if len(self.__strbuffer) == 0 or not self.__append:
            self.__strbuffer.append('\e[')
            self.__append = True
        self.__color(key, 'black', 30, 40)
        self.__color(key, 'red', 31, 41)
        self.__color(key, 'green', 32, 42)
        self.__color(key, 'yellow', 33, 43)
        self.__color(key, 'blue', 34, 44)
        self.__color(key, 'purple', 35, 45)
        self.__color(key, 'darkgreen', 36, 46)
        self.__color(key, 'white', 37, 47)
        if key == 'consle':
            self.__strbuffer.append('0m')
        if key == 'hg':
            self.__strbuffer.append('1m')
        if key == 'low':
            self.__strbuffer.append('0m')
        return self

    def __color(self, key, color, fore_gruod, back_ground):
        if key == color:
            if not self.__fore_color:
                self.__strbuffer.append('%d;' % fore_gruod)
                self.__fore_color = True
            else:
                self.__strbuffer.append('%d;' % back_ground)
                self.__fore_color = False

    def __str__(self):
        if self.__strbuffer and isinstance(self.__strbuffer, list):
            if len(self.__strbuffer) > 0 and self.__strbuffer[len(self.__strbuffer) - 1] != '\e[0m':
                self.__strbuffer.append('\e[0m')
            return ''.join(self.__strbuffer)
        else:
            return ''

    @staticmethod
    def consle_show(sentence):
        call(['echo', '-e', '%s' % sentence])

    @staticmethod
    def consle_clear():
        call(['clear'])

    @staticmethod
    def consle_move(line):
        call(['echo', '-e', '\33[%dC' % (line)])


import sys
import tty
import termios


class Control(object):

    '''
    这个是网络上抄的　，　摘自https://github.com/bfontaine/term2048/blob/master/term2048/keypress.py
    但是其它部分都是原创　，　打小抄了　．．．
    '''
    UP, DOWN, RIGHT, LEFT = 65, 66, 67, 68

    # Vim keys
    K, J, L, H = 107, 106, 108, 104

    __key_aliases = {
        K: UP,
        J: DOWN,
        L: RIGHT,
        H: LEFT,
    }

    __key_map = {65: 'UP',
                 66: 'DOWN',
                 67: 'RIGHT',
                 68: 'LEFT'
                 }

    def __init__(self):
        self.__fd = sys.stdin.fileno()
        self.__old = termios.tcgetattr(self.__fd)

    def __getKey(self):
        """Return a key pressed by the user"""
        try:
            tty.setcbreak(sys.stdin.fileno())
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            ch = sys.stdin.read(1)
            return ord(ch) if ch else None
        finally:
            termios.tcsetattr(self.__fd, termios.TCSADRAIN, self.__old)

    def getKey(self):
        """
        same as __getKey, but handle arrow keys
        """
        k = self.__getKey()
        if k == 27:
            k = self.__getKey()
            if k == 91:
                k = self.__getKey()

        return self.__key_map.get(self.__key_aliases.get(k, k))

from random import randint


class GameArry(object):

    __board = None  # 这是一个一维数组可以模拟二维数组　或者更高维
    __cmd = ConsleString()  # 终端字符串格式化　得到有色字体的利器
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
            self.__board[__r] = 2
            __create += 1

    def __move(self, left, right, step, fi):
        '''
        功能：
        整个数组的移动
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
        '''

        '''
        return self.__move(self.__hard - 2,  -1,
                           -1, lambda x, y, z:  z * y + x)

    def __random(self, min, max):
        return randint(min, max)

    def test(self):
        self.__cmd.red.black.append_string('english')
        print self.__cmd
        ConsleString.consle_show(self.__cmd)
        self.__cmd.clear()

    def __pgame(self):

        ConsleString.consle_clear()
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
            self.__cmd.red.green.append_string(''.join(consle))
            ConsleString.consle_show(self.__cmd)
            # ConsleString.consle_show()

    def start(self):
        '''
        游戏主ｍａｉｎ方法
        游戏开始
        '''

        while self.__islive:
            self.__pgame()
            key = self.__key.getKey()
            if key:
                if getattr(self,  key.lower())():

                    self.__create_point()

    def __islive(self):
        '''
        判断游戏是否可以继续
        判断是否有空格的存在
        判断是否有一个方块与左面相同（其实你在我的右面　等于我的左面的左面）
        判断是否有一个方块于上面一个方块相同
        '''
        for i in range(self.__hard):
            for j in range(self.__hard):
                if self.__board[i * __hard + j] == 0:
                    return True
                elif (i - 1) > 0 and self.__board[(i - 1) * self.__hard + j] == self.__board[i * self.__hard + j]:
                    return True
                elif (j - 1) > 0 and self.__board[i * self.__hard + j] == self.__board[i * self.__hard + j - 1]:
                    return True


if __name__ == '__main__':
    c = GameArry()
    print c.start()
