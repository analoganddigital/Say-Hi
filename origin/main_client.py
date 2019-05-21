# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 12:46:11 2019

@author: pc
"""
import threading
import sys 
import time
import argparse
import struct
import pickle
import zlib

from vchat_server import Video_Server
from vchat_client import Video_Client
parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='10.122.217.38')
parser.add_argument('--port', type=int, default=10089)
parser.add_argument('--level', type=int, default=1)
parser.add_argument('-version', type=int, default=4)

args = parser.parse_args()

IP = args.host
PORT = args.port
VERSION = args.version
LEVEL = args.level

if __name__ == '__main__':
#__name__是指示当前py文件调用方式的方法。如果它等于"__main__"就表示是直接执行，
#如果不是，则用来被别的文件调用，这个时候if就为False，那么它就不会执行最外层的代码了。
    vclient = Video_Client(IP, PORT, LEVEL, VERSION)
    #vserver = Video_Server(PORT, VERSION)
    #vserver.start()
    vclient.start()
    time.sleep(1)
    while True:
        time.sleep(1)
        if not vclient.isAlive():
            print("Video connection lost ...")
            sys.exit(0)
            