# coding=utf-8
#!/usr/bin/env python


from optparse import OptionParser
import sys
from subprocess import call


class ConsleString(object):

    __strbuffer = []
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


class Control(object):
    import sys
    import tty
    import termios

    UP, DOWN, RIGHT, LEFT = 65, 66, 67, 68

    # Vim keys
    K, J, L, H = 107, 106, 108, 104

    __key_aliases = {
        K: UP,
        J: DOWN,
        L: RIGHT,
        H: LEFT,
    }

    def __init__(self):
        self.__fd = sys.stdin.fileno()
        self.__old = termios.tcgetattr(__fd)

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

        return self.__key_aliases.get(k, k)

from random import randint


class GameArry(object):

    __board = None
    __cmd = ConsleString()
    __score = 0

    def __init__(self, array_len=4):
        self.array_len = array_len
        self.reset()

    def reset(self):
        if not self.array_len:
            self.array_len = 4
        elif not (isinstance(self.array_len, int) and self.array_len >= 4 and self.array_len <= 8):
            self.array_len = 4
        self.__board = [0 for _ in range(self.array_len * self.array_len)]
        self.__score = 0
        self.__create_point(2)

    def __create_point(self , n = 1):
        for i in range(n):
            __r = self.__random(0, len(self.__board) - 1)
            if self.__board[__r] != 0:
                i = i - 1
                continue
            self.__board[__r] = 2

    def __move(self, left, right, step, fi):
        for i in range(left, right, step):
            for rl in range(self.array_len):
                for j in range(left, i, step):
                    __index = fi(i, self.array_len, rl)
                    __next = fi(j, self.array_len, rl)
                    if self.__board[__index] == self.__board[__next] or self.__board[__next] == 0:
                        self.__board[
                            __next] += self.__board[__index]
                        self.__score += self.__board[__index]
                        self.__board[__index] = 0
                        break

    def down(self):
        self.__move(self.array_len - 1,  -1,
                    -1, lambda x, y, z: x * y + z)

    def up(self):
        self.__move(0, self.array_len, 1, lambda x, y, z: x * y + z)

    def left(self):
        self.__move(0, self.array_len, 1, lambda x, y, z:  z * y + x)

    def right(self):
        self.__move(self.array_len - 1,  -1,
                    -1, lambda x, y, z:  z * y + x)

    def __random(self, min, max):
        return randint(min, max)

    def p(self):
        for i in range(self.array_len):
            print self.__board[i * self.array_len: (i + 1) * self.array_len]


if __name__ == '__main__':
    print range(4, 1, -1)
    c = GameArry()
    print c.p()
    c.down()
    print c.p()
    c.up()
    print c.p()
    c.down()
    print c.p()
    c.left()
    print c.p()
    c.left()
    print c.p()
    print range(1, 4)
