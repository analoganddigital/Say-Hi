# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:16:23 2019

@author: pc
"""

import tkinter as tk
import threading
import os
import time

class print_chinese(threading.Thread):
    def __init__(self, audio_tran_ch, update_time, break_txt):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.window = tk.Tk()
        self.window.title('Chating')
        self.window.geometry('500x300')
        self.print_desk = tk.Text(self.window, height=18, width=60)
        self.print_desk.pack()
        self.print_desk.place(x=40,y=20)
        self.audio_tran_ch = audio_tran_ch
        self.update_time = update_time
        self.break_txt = break_txt
        
    def __del__(self):
        self.window.quit() 
        print("window close")
        return 0   

    def get(self):
        while True:
            if os.path.exists(self.break_txt) is True:
                break
            else:
                time1 = time.time()
                while True:
                    time2 = time.time()
                    if abs(int(time2)-int(time1)) > self.update_time:
                        if os.path.exists(self.audio_tran_ch):
                            audio_content = open(self.audio_tran_ch)
                            chinese = audio_content.read()
                            audio_content.close()
                            self.print_desk.insert('insert', chinese)
                            break
                    self.window.update()
        

if __name__ == '__main__':
    p = print_chinese("C:/Users/pc/Desktop/program_edit/program/audio_tran_ch/audio_tran_ch.txt",3)
    p.start()
    p.get()