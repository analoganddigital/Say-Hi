# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:11:45 2019

@author: pc
"""


import tkinter as tk  
from main_edit_2 import main_edit_2
#import main_edit

butt = False
    
def insert_point(): # 在鼠标焦点处插入输入内容
    global butt
    if butt == False:
        butt = True
        PC_v = PC_var.get()
        IP_add = IP.get()
        level_v = level_var.get()
        face_capture = face_var.get()
        audio_tran = audio_var.get()
        view_v = view_var.get()
        print_desk.insert('insert', "get PC: " + PC_v + "\n")
        print_desk.insert('insert', "get server IP: " + IP_add + "\n")
        print_desk.insert('insert', "get level: " + level_v + "\n")
        print_desk.insert('insert', "get face capture: " + face_capture + "\n")
        print_desk.insert('insert', "get audio transform: " + audio_tran + "\n")
        print_desk.insert('insert', "get view version: " + view_v + "\n")
        print_desk.insert('insert', "you can print 'q' to close " + "\n")
        main_go = main_edit_2(PC_v, level_v, face_capture, audio_tran, view_v, IP_add)
        #main_edit.main_edit(PC_v, level_v, face_capture, audio_tran, view_v, IP_add)
        main_go.start()
              
# 第1步，实例化object，建立窗口window
window = tk.Tk()
window.title('Say Hi')
window.geometry('500x300')

PC_var = tk.StringVar()    # 定义一个var用来将radiobutton的值和Label的值联系在一起.
PC = tk.Label(window, bg='white', width=10, text='PC:')
PC.pack()
PC.place(x=30,y=0)
 
PC_1 = tk.Radiobutton(window, text='1', variable=PC_var, value=1)
PC_1.pack()
PC_1.place(x=180,y=0)
PC_2 = tk.Radiobutton(window, text='2', variable=PC_var, value=2)
PC_2.pack()
PC_2.place(x=230,y=0)


IP_name = tk.Label(window, text='Server IP:', bg='white', width=10)
IP_name.pack()
IP_name.place(x=30,y=30)
IP = tk.Entry(window, show = None)#显示成明文形式
IP.pack()
IP.place(x=180,y=30)


level_var = tk.StringVar()
level = tk.Label(window, bg='white', width=10, text='Quality:')
level.pack()
level.place(x=30,y=60)
 
level_1 = tk.Radiobutton(window, text='super', variable=level_var, value=0)
level_1.pack()
level_1.place(x=180,y=60)
level_2 = tk.Radiobutton(window, text='high', variable=level_var, value=1)
level_2.pack()
level_2.place(x=240,y=60)
level_3 = tk.Radiobutton(window, text='medium', variable=level_var, value=2)
level_3.pack()
level_3.place(x=290,y=60)
level_4 = tk.Radiobutton(window, text='low', variable=level_var, value=3)
level_4.pack()
level_4.place(x=360,y=60)


face_var = tk.StringVar()
face = tk.Label(window, bg='white', width=18, text='Face Recognition:')
face.pack()
face.place(x=30,y=90)

face_1 = tk.Radiobutton(window, text='open', variable=face_var, value=1)
face_1.pack()
face_1.place(x=180,y=90)
face_2 = tk.Radiobutton(window, text='close', variable=face_var, value=0)
face_2.pack()
face_2.place(x=240,y=90)


audio_var = tk.StringVar()
audio = tk.Label(window, bg='white', width=18, text='Speech Recognition:')
audio.pack()
audio.place(x=30,y=120)

audio_1 = tk.Radiobutton(window, text='open', variable=audio_var, value=1)
audio_1.pack()
audio_1.place(x=180,y=120)
audio_2 = tk.Radiobutton(window, text='close', variable=audio_var, value=0)
audio_2.pack()
audio_2.place(x=240,y=120)

view_var = tk.StringVar()
view = tk.Label(window, bg='white', width=10, text='Style:')
view.pack()
view.place(x=30,y=150)

view_1 = tk.Radiobutton(window, text='natural', variable=view_var, value=0)
view_1.pack()
view_1.place(x=180,y=150)
view_2 = tk.Radiobutton(window, text='cartoon', variable=view_var, value=1)
view_2.pack()
view_2.place(x=250,y=150)
view_3 = tk.Radiobutton(window, text='pencil', variable=view_var, value=2)
view_3.pack()
view_3.place(x=320,y=150)


button = tk.Button(window, text='OK', width=5,
               height=1, command=insert_point)
button.pack()
button.place(x=230,y=260)


print_desk = tk.Text(window, height=6, width=63)
print_desk.pack()
print_desk.place(x=30,y=180)

window.mainloop()
window.quit() 
print("window close")