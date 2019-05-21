# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 22:00:28 2019

@author: pc
"""

from socket import *
import threading
import pyaudio
import time
import struct


import wave
import sys

import zlib

import pickle
import numpy as np


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 0.1

class Audio_Client(threading.Thread):
    def __init__(self, ip, port, version):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = (ip, port)
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6,SOCK_STREAM)
        self.p = pyaudio.PyAudio()
        self.stream = None
    
    def __del__(self):
        self.sock.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        
    def run(self):
        print("AUDIO client starts ...")
        while True:
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(3)
                continue
        print("AUDIO client connected ...")
        self.stream = self.p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)#开始录音
        print("* recording")
        while self.stream.is_active():
            frames = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = self.stream.read(CHUNK)
                frames.append(data)#录音结束
            senddata = pickle.dumps(frames)#打包
            try:
                self.sock.sendall(struct.pack("L",len(senddata))+senddata)
            except:
                break