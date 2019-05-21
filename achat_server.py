# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 23:09:54 2019

@author: pc
"""

from socket import *
import threading
import pyaudio
import time
import struct
import os

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

class Audio_Server(threading.Thread):
    def __init__(self, port, version, audio_save, audio_break, Audio_time):
        threading.Thread.__init__(self)
        self.setDaemon(True)#使每个线程在主线程结束后自动退出，保证程序不会崩溃且无法销毁的情况
        self.ADDR = ('',port)#端口号
        self.audio_save = audio_save
        self.audio_break = audio_break
        self.Audio_time = Audio_time
        if version == 4:#IPV4 or IPV6
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
        print("audio close")
        
    def run(self):
        print("AUDIO server starts ...")
        self.sock.bind(self.ADDR)#端口监听
        self.sock.listen(1)
        conn, addr = self.sock.accept()#与用户端连接
        print("remote AUDIO client success connected ...")
        data = "".encode("utf-8")#接收数据
        payload_size = struct.calcsize("L")#记录当前缓冲区的数据长度，准确提取每一帧
        self.stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
        while True:
            if os.path.exists(self.audio_break):
                break
            else:
                frames_AI = []
                time1=time.time()#获取前进时的时间
                while True:
                    time2=time.time()
                    while len(data) < payload_size:#超过数据流的部分被截取掉，和下一次合并整合，不足时将合并下一帧到该帧
                        data += conn.recv(81920)
                    packed_size = data[:payload_size]#从最初剪到指定位置，剪切操作，剪切到一个完整的一帧
                    data = data[payload_size:]#从指定位置剪切到末尾
                    msg_size = struct.unpack("L",packed_size)[0]#解压前面的头
                    while len(data) < msg_size:
                        data += conn.recv(89120)
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frames = pickle.loads(frame_data)#frames为str形式
                    for frame in frames:
                        self.stream.write(frame, CHUNK)#从frame中读数据，然后写到stream中。就是从文件中读取数据然后写到声卡里
                        frames_AI.append(frame)
                    if abs(int(time2)-int(time1)) > self.Audio_time:
                        break
                wf = wave.open(self.audio_save, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames_AI))
                wf.close()
                print("audio save")
                
        