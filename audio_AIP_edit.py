# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:39:06 2019

@author: pc
"""

from aip import AipSpeech
import threading
import time
import os
import wave
import pyaudio

class Audio_AIP(threading.Thread):
    def __init__(self, APP_ID, API_KEY, SECRET_KEY, filepath_get, break_audio, audio_tran_ch):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        self.FilePath = filepath_get
        self.break_audio = break_audio
        self.audio_tran_ch = audio_tran_ch
        print("AIP is ready")

    def get_file_content(self, filePath):
        cmd_str = "ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s.pcm"%(filePath,filePath)
        os.system(cmd_str)  # 调用系统命令ffmpeg,传入音频文件名即可
        with open(filePath + ".pcm", 'rb') as fp:
            return fp.read()
        
    def run(self):
        while True:
            if os.path.exists(self.FilePath) is True:
                if os.path.exists(self.break_audio) is True:
                    break
                else:
                    a = self.client.asr(self.get_file_content(self.FilePath), 'pcm', 16000, {'dev_pid': 1536,})
                    if a.get('err_no') == 0:
                        file_audio_save = open(self.audio_tran_ch, 'w')
                        save = a.get('result')[0] + "\n"
                        file_audio_save.write(save)
                        file_audio_save.close()
                        print(a.get('result')[0])
                        print("already save")
                    else:
                        print("error or empty")
                    time.sleep(5)
                    
    def __del__(self):
        print("AIP close")
        return 0