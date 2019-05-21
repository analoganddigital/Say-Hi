# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:47:22 2019

@author: pc
"""

import sys 
import time
import argparse
import os

from vchat_server import Video_Server
from vchat_client import Video_Client
from achat_server import Audio_Server
from achat_client import Audio_Client
from audio_AIP_edit import Audio_AIP

APP_ID = '15920162'
API_KEY = 'kbpGI9bdy39Isbn7sQQGzQQV'
SECRET_KEY = 'jZ6N1ti0GyzPWGeuooU3ing7flHjjrWh'
WAVE_OUTPUT_FILENAME = "C:/Users/pc/Desktop/program_edit/program/audio/output.wav"
FACE_SHAPE_PREDICTOR = "C:/Users/pc/Desktop/program_edit/program/shape_predictor_68_face_landmarks.dat"
BREAK_AUDIO_AIP = "C:/Users/pc/Desktop/program_edit/program/break_audio_aip/break_aduio.txt"

if os.path.exists(BREAK_AUDIO_AIP):
    os.remove(BREAK_AUDIO_AIP)
    
if os.path.exists(WAVE_OUTPUT_FILENAME):
    os.remove(WAVE_OUTPUT_FILENAME)
    
parser = argparse.ArgumentParser()
PC_V = int(input("input PC-version(1 or 2):"))
print("get PC:", PC_V, "as client")

Level = int(input("choose level(0 to 3):"))#越低显示效果越好
print("get level:", Level)

face_c = int(input("start face_capture(0 or 1):"))
if face_c == 1:
    print("face_capture is open")
else:
    print("face_capture is close")
    
audio_t = int(input("start audio_trans(0 or 1):"))
if audio_t == 1:
    print("audio_trans is open")
else:
    print("audio_trans is close")
    
view_ver = int(input("choose a view(0 for normal;1 for cartoon;2 for pencil):"))
if view_ver == 0:
    print("view is normal")
elif view_ver == 1:
    print("view is cartoon")
elif view_ver == 2:
    print("view is pencil")

if PC_V == 2:
    host1 = str(input("input server_IP:"))
    print("get server_IP:", host1)
    parser.add_argument('--host_PC1', type=str, default=host1)
    
elif PC_V == 1:
    host2 = str(input("input server_IP:"))
    print("get server_IP:", host2)
    parser.add_argument('--host_PC2', type=str, default=host2)
    
parser.add_argument('--port_PC1', type=int, default=10486)
parser.add_argument('--level_PC1', type=int, default=Level)
parser.add_argument('--version_PC1', type=int, default=4)
parser.add_argument('--face_PC1', type=int, default=face_c)
parser.add_argument('--view_version_PC1', type=int, default=view_ver)


parser.add_argument('--port_PC2', type=int, default=10487)
parser.add_argument('--level_PC2', type=int, default=Level)
parser.add_argument('--version_PC2', type=int, default=4)
parser.add_argument('--face_PC2', type=int, default=face_c)
parser.add_argument('--view_version_PC2', type=int, default=view_ver)

parser.add_argument('--port_PC1_A', type=int, default=10488)
parser.add_argument('--port_PC2_A', type=int, default=10489)

parser.add_argument('--AppID', type=str, default=APP_ID)
parser.add_argument('--APIkey', type=str, default=API_KEY)
parser.add_argument('--Secret_Key', type=str, default=SECRET_KEY)
parser.add_argument('--Filepath', type=str, default=WAVE_OUTPUT_FILENAME)
parser.add_argument('--Break_Audio', type=str, default=BREAK_AUDIO_AIP)

parser.add_argument('--Face_Shape_Predictor', type=str, default=FACE_SHAPE_PREDICTOR)

args = parser.parse_args()

if PC_V == 2:
    IP_PC1 = args.host_PC1
elif PC_V == 1:
    IP_PC2 = args.host_PC2

PORT_PC1 = args.port_PC1
VERSION_PC1 = args.version_PC1#IPv4还是IPv6
LEVEL_PC1 = args.level_PC1
FACE_PC1 = args.face_PC1
VIEW_PC1 = args.view_version_PC1

PORT_PC2 = args.port_PC2
VERSION_PC2 = args.version_PC2
LEVEL_PC2 = args.level_PC2
FACE_PC2 = args.face_PC2
VIEW_PC2 = args.view_version_PC2

PORT_PC1_A = args.port_PC1_A
PORT_PC2_A = args.port_PC2_A

app_id = args.AppID
apikey = args.APIkey
secret_key = args.Secret_Key
filepath = args.Filepath
break_audio = args.Break_Audio

face_shape_predictor = args.Face_Shape_Predictor

if __name__ == '__main__':
#__name__是指示当前py文件调用方式的方法。如果它等于"__main__"就表示是直接执行，
#如果不是，则用来被别的文件调用，这个时候if就为False，那么它就不会执行最外层的代码了。
    if PC_V == 2:#pc1为客户端
        vclient_PC1 = Video_Client(IP_PC1, PORT_PC1, LEVEL_PC1, VERSION_PC1)#PC1作为客户端
        vserver_PC2 = Video_Server(PORT_PC2, VERSION_PC2, FACE_PC2, VIEW_PC2, face_shape_predictor)#PC1作为服务器端，PC2作为客户端
        aclient_PC1 = Audio_Client(IP_PC1, PORT_PC1_A, VERSION_PC1)
        aserver_PC2 = Audio_Server(PORT_PC2_A, VERSION_PC2, filepath)
        audio_trans = Audio_AIP(app_id, apikey, secret_key, filepath, break_audio)
        vserver_PC2.start()
        aserver_PC2.start()
        time.sleep(1)
        vclient_PC1.start()
        aclient_PC1.start()
        if audio_t == 1:
            audio_trans.start()
        while True:
            time.sleep(1)
            if not vclient_PC1.isAlive() or not vserver_PC2.isAlive():
                print("Video connection lost ...")
                file = open(break_audio,'w')
                sys.exit(0)
            if not aclient_PC1.isAlive() or not aserver_PC2.isAlive():
                print("Audio connection lost ...")
                file = open(break_audio,'w')
                sys.exit(0)
                
    elif PC_V == 1:#pc2为客户端
        vclient_PC2 = Video_Client(IP_PC2, PORT_PC2, LEVEL_PC2, VERSION_PC2)#PC2作为客户端
        vserver_PC1 = Video_Server(PORT_PC1, VERSION_PC1, FACE_PC1, VIEW_PC1, face_shape_predictor)#PC2作为服务器端，PC1作为客户端
        aclient_PC2 = Audio_Client(IP_PC2, PORT_PC2_A, VERSION_PC2)
        aserver_PC1 = Audio_Server(PORT_PC1_A, VERSION_PC1, filepath)
        audio_trans = Audio_AIP(app_id, apikey, secret_key, filepath, break_audio)
        vserver_PC1.start()
        aserver_PC1.start()
        time.sleep(1)
        vclient_PC2.start()
        aclient_PC2.start()
        if audio_t == 1:
            audio_trans.start()
        while True:
            time.sleep(1)
            if not vclient_PC2.isAlive() or not vserver_PC1.isAlive():
                print("Video connection lost ...")
                file = open(break_audio,'w')
                sys.exit(0) 
            if not aclient_PC2.isAlive() or not aserver_PC1.isAlive():
                print("Audio connection lost ...")
                file = open(break_audio,'w')
                sys.exit(0)
                