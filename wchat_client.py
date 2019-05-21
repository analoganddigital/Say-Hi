# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 12:30:35 2019

@author: pc
"""

from socket import *
import threading
import time
import tkinter as tk
import os

b='10.122.232.226'
a='C:/Users/pc/Desktop/program_edit/program/word_ch/word_ch.txt'
c='C:/Users/pc/Desktop/program_edit/program/break_audio/break_aduio.txt'

class Word_Client(threading.Thread):
    def __init__(self, ip, port, version, word_chat):
        threading.Thread.__init__(self)
        self.setDaemon(True)#使每个线程在主线程结束后自动退出，保证程序不会崩溃且无法销毁的情况
        self.ADDR = (ip, port)#服务器端IP地址及端口号
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)#创建套接字
        else:
            self.sock = socket(AF_INET6,SOCK_STREAM)
        self.window = tk.Tk()
        self.window.title('Word_Chating')
        self.window.geometry('500x300')
        
        self.print_desk = tk.Text(self.window, height=14, width=60)
        self.print_desk.pack()
        self.print_desk.place(x=40,y=20)
        
        self.input_name = tk.Label(self.window, text='Input Word:', bg='white', width=12)
        self.input_name.pack()
        self.input_name.place(x=40,y=210)
        self.input_desk = tk.Entry(self.window, show = None)#显示成明文形式
        self.input_desk.pack()
        self.input_desk.place(x=150,y=210)
        
        self.button = tk.Button(self.window, text='INPUT', width=5,
               height=1, command=self.insert_word)
        self.button.pack()
        self.button.place(x=230,y=250)
        
        self.word_chat = word_chat
        
    def send_word(self):
        print("WORD client starts ...")
        while True:
            try:
                self.sock.connect(self.ADDR)#发送一个连接建立请求报文段
                break
            except:
                time.sleep(3)
                continue
        print("WORD client connected ...")
        #conn, addr = self.sock.accept()#与用户端连接
        while True:
            if os.path.exists(self.word_chat):
                if self.sock.recv(1024).decode() == '1':
                    word_content = open(self.word_chat)
                    word = word_content.read()
                    word_content.close()
                    self.print_desk.insert('insert', word)
                    os.remove(self.word_chat)
                    print("remove")
            self.window.update()
        
    def insert_word(self):
        Word = self.input_desk.get()
        #self.input_desk.delete('1.0','end')
        self.print_desk.insert('insert', "my PC: " + Word + "\n")
        sentence = "opposite PC:" + Word
        self.sock.send(sentence.encode())
        
    def __del__(self):
        os.remove(self.word_chat)
        self.sock.close()
        self.window.quit() 
        print("window close")
        return 0   

if __name__ == '__main__':
    k = Word_Client(b,10080,4,a)    
    k.start() 
    k.send_word()
        
        