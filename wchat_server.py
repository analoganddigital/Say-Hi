# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 13:37:18 2019

@author: pc
"""

from socket import *
import threading
import time
import os

b='10.122.232.226'
a='C:/Users/pc/Desktop/program_edit/program/word_ch/word_ch.txt'
c='C:/Users/pc/Desktop/program_edit/program/break_audio/break_aduio.txt'

class Word_Server(threading.Thread):
    def __init__(self, port, version, word_save):
        threading.Thread.__init__(self)
        self.setDaemon(True)#使每个线程在主线程结束后自动退出，保证程序不会崩溃且无法销毁的情况
        self.ADDR = ('',port)#指定套接字端口号
        if version == 4:#IPV4 or IPV6
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6,SOCK_STREAM)
        self.word_save = word_save
    
    def __del__(self):
        self.sock.close()
        print("word server close")
    
    def run(self):
        print("WORD server starts ...")
        self.sock.bind(self.ADDR)#关联特定的端口号
        self.sock.listen(1)#监听
        conn, addr = self.sock.accept()#服务器端创建新的套接字，与用户端连接
        print("remote WORD client success connected ...")
        while True:
            sentence = conn.recv(1024).decode()
            if sentence is not None:
                file_word_save = open(self.word_save, 'w')
                save = sentence + "\n"
                file_word_save.write(save)
                file_word_save.close()
                print("already save")
                answer = "1"
                conn.send(answer.encode())
                print("send get")
        
if __name__ == '__main__':
    k = Word_Server(10080,4,a)
    k.start()
    #k.get_word()
        