# -*- coding: utf-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### Alias : console.keyboard & Last Modded : 2021.05.05. ###
Coded with Python 3.9 for Windows (CRLF) by IRACK000
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from console.util import ConsoleAPI
import console.showboard as sb
import sockets.logserver as log

from threading import Thread  # https://monkey3199.github.io/develop/python/2018/12/04/python-pararrel.html


class Buffered_ConsoleAPI(ConsoleAPI):
    __buffer = []
    __buffer_on = False
    __thread = None
    __mutex = False
    __stop_thread = True

    @classmethod
    def __watchdog(cls, id, getch, buffer):
        while not cls.__stop_thread:
            c = getch()
            if type(c) != str:
                c = c.decode('utf-8')
            if c == '\003':
                raise KeyboardInterrupt
            buffer.append(c)

    @classmethod
    def runthread(cls):
        cls.__buffer_on = True
        cls.__stop_thread = False
        if cls.__thread is None:
            cls.__thread = Thread(target=cls.__watchdog, args=(
                2, cls.getch, cls.__buffer
            ))
        cls.__thread.start()
        log.send("Keyboard Thread started", 2)

    @classmethod
    def stopthread(cls):
        cls.__buffer_on = False
        cls.__stop_thread = True
        print("\u001B[6n", end='', flush=True)
        cls.__thread.join()
        while True:
            c = cls.getch()
            if type(c) != str:
                c = c.decode('utf-8')
            if c == 'R':
                break
        log.send("Keyboard Thread stoped", 2)

    @classmethod
    def buf_getch(cls):
        if not cls.getcodepage() or not cls.__buffer_on:
            return super(Buffered_ConsoleAPI, cls).getch()
        if cls.__mutex:
            return "Locked"
        cls.__mutex = True
        if len(cls.__buffer) != 0:
            c = cls.__buffer.pop(0)
            cls.__mutex = False
            return c
        else:
            cls.__mutex = False
            return None

    @classmethod
    def wrisxy(cls):
        """get console cursor position. {'x': x, 'y': y}"""
        if not cls.__unicode or not cls.__buffer_on:
            return super(Buffered_ConsoleAPI, cls).wrisxy()
        while cls.__mutex:
            pass
        cls.__mutex = True
        index = len(cls.__buffer)
        print("\u001B[6n", end='', flush=True)
        get = []
        while True:
            try:
                c = cls.__buffer.pop(index)
            except Exception:
                break
            if c == 'R':
                x = int(''.join(get))
                break
            elif c == ';':
                y = int(''.join(get))
                get.clear()
            elif c >= '0' and c <= '9':
                get.append(c)
        cls.__mutex = False
        return {'x': x, 'y': y}

    @classmethod
    def pause(cls, prompt="Press any key to continue . . ."):
        """pause console"""
        # https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space
        if not cls.__buffer_on:
            return super(Buffered_ConsoleAPI, cls).pause(prompt)
        print(prompt, end='', flush=True)
        while True:
            c = cls.buf_getch()
            if c == "Locked" and c is None:
                continue
            else:
                print()
                break

    @classmethod
    def getpass(cls, prompt='Password: ', stream=None):
        """Prompt for password with echo off"""
        # 참고 : https://www.programcreek.com/python/example/51346/msvcrt.putch
#        if sys.stdin is not sys.__stdin__:
#            return fallback_getpass(prompt, stream)
        if not cls.__buffer_on:
            return super(Buffered_ConsoleAPI, cls).getpass(prompt, stream)
        while cls.__mutex:
            pass
        cls.__mutex = True
        index = len(cls.__buffer)
        print(prompt, end='', flush=True)
        pw = ""
        while True:
            try:
                c = cls.__buffer.pop(index)
            except Exception:
                break
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


def interrupt(id, tr):
    global quit
    Buffered_ConsoleAPI.runthread()
    getch = Buffered_ConsoleAPI.buf_getch
    while not quit:
        c = getch()
        if c == "Locked" and c is None:
            continue
        if c == 'q':
            quit = True
            log.send("Quit Command Input")
            break
        elif c == 'n':
            tr.nextsignal()
            sb.print_trafficsystem(tr.getstatus())
        elif c == 'l':
            if not log.logging:
                log.on()
            else:
                log.off()


def run(cnu_tr):
    global thread
    global quit
    quit = False
    thread = Thread(target=interrupt, args=(1, cnu_tr))
    thread.start()
    log.send("Interrupt Thread started", 2)


def stop():
    global quit
    quit = True
    Buffered_ConsoleAPI.stopthread()
    thread.join()
