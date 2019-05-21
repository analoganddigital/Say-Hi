# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 19:16:16 2019

@author: pc
"""

from socket import *
import threading
import time
import cv2
import struct
import pickle
import zlib
import cartoon_edit
import face_capture_edit
import pencil_edit

class Video_Server(threading.Thread):
    def __init__ (self, port, version, face_cap, view_version, face_shape_predictor, break_audio_aip, break_audio):
        threading.Thread.__init__(self)
        self.setDaemon(True)#使每个线程在主线程结束后自动退出，保证程序不会崩溃且无法销毁的情况
        self.ADDR = ('',port)#指定套接字端口号
        self.face_cap = face_cap
        self.view_version = view_version
        self.face_shape_predictor = face_shape_predictor
        self.break_audio = break_audio
        self.break_audio_aip = break_audio_aip
        if version == 4:#IPV4 or IPV6
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6,SOCK_STREAM)
            
    def __del__(self):
        self.sock.close()
        try:
            cv2.destoryALLWindows()
        except:
            pass
        print("video close")
    
    def run(self):
        detector, predictor = face_capture_edit.face_init(self.face_shape_predictor) 
        print("face_capture_init is ready")
        print("VIDEO server starts ...")
        self.sock.bind(self.ADDR)#关联特定的端口号
        self.sock.listen(1)#监听
        conn, addr = self.sock.accept()#服务器端创建新的套接字，与用户端连接
        print("remote VIDEO client success connected ...")
        data = "".encode("utf-8")#接收数据
        payload_size = struct.calcsize("L")#记录当前缓冲区的数据长度，准确提取每一帧
        cv2.namedWindow('Remote',cv2.WINDOW_NORMAL)
        while True:
            while len(data) < payload_size:#超过数据流的部分被截取掉，和下一次合并整合，不足时将合并下一帧到该帧
                data +=conn.recv(81920)
            packed_size = data[:payload_size]#从最初剪到指定位置，剪切操作，剪切到一个完整的一帧
            data = data[payload_size:]#从指定位置剪切到末尾
            msg_size = struct.unpack("L",packed_size)[0]#解压前面的头
            while len(data) < msg_size:
                data += conn.recv(89120)
            zframe_data = data[:msg_size]
            data = data[msg_size:]
            frame_data = zlib.decompress(zframe_data)
            frame = pickle.loads(frame_data)
            if self.face_cap == 1:
                frame_face = face_capture_edit.face_capture_e(frame.copy(),detector, predictor)
                cv2.imshow("Face_capture", frame_face)
            if self.view_version == 0:#不变样式
                frame = frame
            elif self.view_version == 1:#漫画
                frame = cartoon_edit.cartoon_e(frame)
            elif self.view_version == 2:#铅笔画
                frame = pencil_edit.rgb_to_sketch(frame)
            cv2.namedWindow("Remote",0);
            cv2.resizeWindow("Remote", 640, 480);
            cv2.imshow("Remote", frame)
            if cv2.waitKey(1) & 0xff == ord('q'):
                file_aip = open(self.break_audio_aip,'w')
                file_audio = open(self.break_audio,'w')
                break
            