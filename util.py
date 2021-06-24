# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : console.util & Last Modded : 2021.05.05. ###
Coded with Python 3.9 (LF line ending) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 참고 : https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
# 참고 : https://pypi.org/project/ansiescapes/
# 참고 : https://pypi.org/project/getch/

import os
import sys

sys.path.append(os.path.dirname(__file__))
import winAPI


class ConsoleAPI(object):
    __unicode = True

    BLACK = 30
    BLUE = 34
    GREEN = 32
    CYAN = 36
    RED = 31
    PURPLE = 35
    YELLOW = 33
    WHITE = 37
    GREY = 90
    BRIGHT_BLUE = 94
    BRIGHT_GREEN = 92
    BRIGHT_CYAN = 96
    BRIGHT_RED = 91
    BRIGHT_PURPLE = 95
    BRIGHT_YELLO = 93
    BRIGHT_WHITE = 97

    B_BLACK = 40
    B_BLUE = 44
    B_GREEN = 42
    B_CYAN = 46
    B_RED = 41
    B_PURPLE = 45
    B_YELLOW = 43
    B_WHITE = 47
    B_GREY = 100
    B_BRIGHT_BLUE = 104
    B_BRIGHT_GREEN = 102
    B_BRIGHT_CYAN = 106
    B_BRIGHT_RED = 101
    B_BRIGHT_PURPLE = 105
    B_BRIGHT_YELLO = 103
    B_BRIGHT_WHITE = 107

    """
    '검정색': 0, '파란색': 1, '초록색': 2, '옥색': 3, '빨간색': 4, '자주색': 5,
    '노란색': 6, '흰색': 7, '회색': 8, '연한파란색': 9, '연한초록색': 10,
    '연한옥색': 11, '연한빨간색': 12, '연한자주색': 13, '연한노란색': 14, '진한흰색': 15
    """
    TCLR = [BLACK, BLUE, GREEN, CYAN, RED,
            PURPLE, YELLOW, WHITE, GREY, BRIGHT_BLUE, BRIGHT_GREEN,
            BRIGHT_CYAN, BRIGHT_RED, BRIGHT_PURPLE, BRIGHT_YELLO, BRIGHT_WHITE]
    BCLR = [B_BLACK, B_BLUE, B_GREEN, B_CYAN, B_RED,
            B_PURPLE, B_YELLOW, B_WHITE, B_GREY, B_BRIGHT_BLUE, B_BRIGHT_GREEN,
            B_BRIGHT_CYAN, B_BRIGHT_RED, B_BRIGHT_PURPLE, B_BRIGHT_YELLO, B_BRIGHT_WHITE]
    OBJCLR = [BLUE, GREEN, CYAN, RED, PURPLE, YELLOW, BRIGHT_BLUE,BRIGHT_GREEN,
              BRIGHT_CYAN, BRIGHT_RED, BRIGHT_PURPLE, BRIGHT_YELLO]

    NORMAL = 0
    BOLD = 1
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    SHADE = 7
    CANCLE = 9
    UNDERLINE2 = 21

    try:
        import msvcrt as gc
    except ModuleNotFoundError:
        os.system("pip3 install getch")
        import getch as gc
#    getch = gc.getch
#    getche = gc.getche

    @classmethod
    def getch(cls):
        """input char without typing enter & invisible input"""
        return cls.gc.getch()

    @classmethod
    def getche(cls):
        """input char without typing enter & visible input"""
        return cls.gc.getche()

    @classmethod
    def gotoxy(cls, x, y):
        """move console cursor to x, y"""
        if not cls.__unicode:
            winAPI.gotoXY(x-1, y-1)
            return
        print("%c[%d;%df" % (0x1B, y, x), end='', flush=True)

    @classmethod
    def hidecurs(cls, on=False):
        """hidecurs(True) : hide console cursor
           hidecurs(False) : show console cursor"""
        if not cls.__unicode:
            winAPI.hideConsoleCursor(1 if on else 0)
            return
        print("\u001B[?25l" if on else "\u001B[?25h")

    @classmethod
    def wrisxy(cls):
        """get console cursor position. {'x': x, 'y': y}"""
        if not cls.__unicode:
            return {'x': winAPI.wrIsX()+1, 'y': winAPI.wrIsY()+1}
        print("\u001B[6n", end='', flush=True)
        get = []
        while True:
            c = cls.getch()
            if type(c) != str:
                c = c.decode('utf-8')
            if c == 'R':
                x = int(''.join(get))
                break
            elif c == ';':
                y = int(''.join(get))
                get.clear()
            elif c >= '0' and c <= '9':
                get.append(c)
        return {'x': x, 'y': y}

    @classmethod
    def pause(cls, prompt="Press any key to continue . . ."):
        """pause console"""
        # 참고 : https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space
        print(prompt, end='', flush=True)
        try:
            cls.getch()
            print()
        except Exception:
            print()
            raise KeyboardInterrupt

    @classmethod
    def clear(cls):
        if os.name in ('nt', 'dos'):
            os.system("cls")
        elif os.name in ('linux', 'osx', 'posix'):
            os.system("clear")
        else:
            print("\033[H\033[J" if cls.__unicode else "\n" * 120)

    @classmethod
    def getpass(cls, prompt='Password: ', stream=None):
        """Prompt for password with echo off"""
        # 참고 : https://www.programcreek.com/python/example/51346/msvcrt.putch
#        if sys.stdin is not sys.__stdin__:
#            return fallback_getpass(prompt, stream)
        print(prompt, end='', flush=True)
        pw = ""
        while True:
            c = cls.getch()
            if type(c) != str:
                c = c.decode('utf-8')
            if c == '\r' or c == '\n':
                break
            if c == '\003':
                raise KeyboardInterrupt
            if c == '\b':
                pw = pw[:-1]
            else:
                pw = pw + c
        print()
        return pw

    @classmethod
    def printcs(cls, txt="", *args, end='\n'):
        """printcs(txt, x, y, attr, end)
           if args length is 1, then attr=args[0]
           if args length is 2, then x=args[0], y=args[1]
           if args length is 3, then x=args[0], y=args[1], attr=args[2]"""
        if len(args) == 0:
            print(txt, end=end)
        elif len(args) == 1:
            attr = args[0]
            if not cls.__unicode:
                if attr in cls.TCLR:
                    attr = cls.TCLR.index(attr)
                elif attr in cls.BCLR:
                    attr = cls.BCLR.index(attr) * 16 + 15
                winAPI.changeTxtColor(attr)
                print(txt, end=end)
                return
            print("\033[%dm%s\033[0m" % (attr, txt), end=end, flush=True)
        elif len(args) == 2:
            x = args[0]
            y = args[1]
            if not cls.__unicode:
                winAPI.gotoXY(x-1, y-1)
                print(txt, end=end, flush=True)
                return
            print("%c[%d;%dH%s" % (0x1B, y, x, txt), end=end, flush=True)
        elif len(args) == 3:
            x = args[0]
            y = args[1]
            attr = args[2]
            if not cls.__unicode:
                if attr in cls.TCLR:
                    attr = cls.TCLR.index(attr)
                elif attr in cls.BCLR:
                    attr = cls.BCLR.index(attr) * 16 + 15
                winAPI.gotoXY(x-1, y-1)
                winAPI.changeTxtColor(attr)
                print(txt, end=end)
                return
            print("\033[%dm\033[%d;%dH%s\033[0m" % (attr, y, x, txt), end=end, flush=True)
        else:
            raise ValueError("Wrong arguments. len(args) shuld be 0~3.")

    @classmethod
    def setcodepage(cls, unicode=True):
        """use/not use unicode setunicode(True/false)"""
        if type(unicode) != bool:
            print("Wrong arguments.")
            return -1
        if not unicode:
            if not os.name == 'nt':
                print("Unsupported function in your OS")
                return -1
        cls.__unicode = unicode

    @classmethod
    def getcodepage(cls):
        return cls.__unicode


if __name__ == '__main__':
    CS = ConsoleAPI
    if input("Do you want to run in Unicode mode? (yes : y) : ") != 'y':
        CS.setcodepage(unicode=False)
    a = CS.getpass()
    print(a)
    CS.printcs("Hello World________________________________________________", 1, 1)
    CS.printcs("Hello World________________________________________________", 2, 2)
    CS.pause()
    print(CS.wrisxy())
    for i in CS.TCLR:
        CS.printcs(str(i), i)
    for i in CS.BCLR:
        CS.printcs(str(i), i)
    if not CS.getcodepage():
        CS.printcs("", CS.WHITE, end='')
    CS.pause()
    print(CS.wrisxy())
    CS.pause()
