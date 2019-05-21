# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 16:57:35 2019

@author: pc
"""

import threading
from wchat_server import Word_Server
from wchat_client import Word_Client
class word_run_server(threading.Thread):
    def __init__(self, port, version, word_save):
        threading.Thread.__init__(self)
        self.setDaemon(True)#使每个线程在主线程结束后自动退出，保证程序不会崩溃且无法销毁的情况
        self.wserver_PC = Word_Server(port, version, word_save)
        self.wserver_PC.start()
        
    def run(self):
        self.wserver_PC.get_word()
    
class word_run_client(threading.Thread):
    def __init__(self, ip, port, version, word_chat):
        threading.Thread.__init__(self)
        self.setDaemon(True)#使每个线程在主线程结束后自动退出，保证程序不会崩溃且无法销毁的情况
        self.wclient_PC = Word_Client(ip, port, version, word_chat)
        self.wclient_PC.start()
        
    def run(self):
        self.wclient_PC.send_word()