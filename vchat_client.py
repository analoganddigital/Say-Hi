# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 13:17:40 2019

@author: pc
"""

from socket import *
import threading
import time
import cv2
import struct
import pickle
import zlib

class Video_Client(threading.Thread):
    def __init__ (self, ip, port, level, version):
        threading.Thread.__init__(self)
        self.setDaemon(True)#使每个线程在主线程结束后自动退出，保证程序不会崩溃且无法销毁的情况
        self.ADDR = (ip, port)#服务器端IP地址及端口号
        if level <= 3:
            self.interval = level
        else:
            self.interval = 3
        self.fx = 1/(self.interval + 1)
        if self.fx < 0.3:
            self.fx = 0.3
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)#创建套接字
        else:
            self.sock = socket(AF_INET6,SOCK_STREAM)
        self.cap = cv2.VideoCapture(0)#打开摄像头
        self.cap.set(3,640) #设置分辨率
        self.cap.set(4,480)
        
    def __del__(self):
        self.sock.close()
        self.cap.release()
        
    def run(self):
        print("VIDEO client starts ...")
        while True:
            try:
                self.sock.connect(self.ADDR)#发送一个连接建立请求报文段
                break
            except:
                time.sleep(3)
                continue
        print("VIDEO client connected ...")
        while self.cap.isOpened():
            ret,frame = self.cap.read()#获取摄像头图像
            if frame is not None:
                #把图片转化为字节流发送，使用pickle.dumps打包
                sframe = cv2.resize(frame, (0, 0), fx = self.fx, fy = self.fx)#图片压缩
                data = pickle.dumps(sframe)
                zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)#图片打包压缩
                try:
                    self.sock.sendall(struct.pack("L",len(zdata)) + zdata)
                    #sendall方法发送，pack方法为每批数据加一个头，用于接受方确认接收数据的长度
                except:
                    break
                for i in range (self.interval):
                    self.cap.read()
                    
