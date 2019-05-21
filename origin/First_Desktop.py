# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 19:44:01 2019

@author: 碓冰娜娜
"""

import tkinter as tk  # 使用Tkinter前需要先导入
#from main_edit_2 import main_edit_2
#import main_edit

#def reply():
#   showinfo(title='新窗口', message=window)
def windowss():      
# 第1步，实例化object，建立窗口window  
    def insert_point(): # 在鼠标焦点处插入输入内容
        global butt
        butt = False
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
           # main_go = main_edit_2(PC_v, level_v, face_capture, audio_tran, view_v, IP_add)
           # main_edit.main_edit(PC_v, level_v, face_capture, audio_tran, view_v, IP_add)
          #  main_go.start()       
      
    window = tk.Tk()
    window.title('My windows')
# 第3步，设定窗口的大小(长 * 宽)
    window.geometry('500x300')  # 这里的乘是小x
    
    PC_var= tk.StringVar()    # 定义一个var用来将radiobutton的值和Label的值联系在一起.
    PC = tk.Label(window, bg='white', width=10, text='PC:')
    PC.pack()
    PC.place(x=40,y=0)
 
    PC_1 = tk.Radiobutton(window, text='1', variable=PC_var, value=1)
    PC_1.pack()
    PC_1.place(x=150,y=0)
    PC_2 = tk.Radiobutton(window, text='2', variable=PC_var, value=2)
    PC_2.pack()
    PC_2.place(x=200,y=0)

    IP_name = tk.Label(window, text='服务器端IP:', bg='white', width=10)
    IP_name.pack()
    IP_name.place(x=40,y=30)
    IP = tk.Entry(window, show = None)#显示成明文形式
    IP.pack()
    IP.place(x=150,y=30)
    
    level_var = tk.StringVar()
    level = tk.Label(window, bg='white', width=10, text='选择清晰度:')
    level.pack()
    level.place(x=40,y=60)
 
    level_1 = tk.Radiobutton(window, text='超清', variable=level_var, value=0)
    level_1.pack()
    level_1.place(x=150,y=60)
    level_2 = tk.Radiobutton(window, text='高清', variable=level_var, value=1)
    level_2.pack()
    level_2.place(x=200,y=60)
    level_3 = tk.Radiobutton(window, text='普通', variable=level_var, value=2)
    level_3.pack()
    level_3.place(x=250,y=60)
    level_4 = tk.Radiobutton(window, text='粗糙', variable=level_var, value=3)
    level_4.pack()
    level_4.place(x=300,y=60)
    
    face_var = tk.StringVar()
    face = tk.Label(window, bg='white', width=15, text='是否打开人脸识别:')
    face.pack()
    face.place(x=40,y=90)

    face_1 = tk.Radiobutton(window, text='是', variable=face_var, value=1)
    face_1.pack()
    face_1.place(x=150,y=90)
    face_2 = tk.Radiobutton(window, text='否', variable=face_var, value=0)
    face_2.pack()
    face_2.place(x=200,y=90)

    audio_var = tk.StringVar()
    audio = tk.Label(window, bg='white', width=15, text='是否打开语音识别:')
    audio.pack()
    audio.place(x=40,y=120)

    audio_1 = tk.Radiobutton(window, text='是', variable=audio_var, value=1)
    audio_1.pack()
    audio_1.place(x=150,y=120)
    audio_2 = tk.Radiobutton(window, text='否', variable=audio_var, value=0)
    audio_2.pack()
    audio_2.place(x=200,y=120)

    
    view_var = tk.StringVar()
    view = tk.Label(window, bg='white', width=12, text='选择视频风格:')
    view.pack()
    view.place(x=40,y=150)

    view_1 = tk.Radiobutton(window, text='原图', variable=view_var, value=0)
    view_1.pack()
    view_1.place(x=150,y=150)
    view_2 = tk.Radiobutton(window, text='漫画版', variable=view_var, value=1)
    view_2.pack()
    view_2.place(x=200,y=150)
    view_3 = tk.Radiobutton(window, text='素描版', variable=view_var, value=2)
    view_3.pack()
    view_3.place(x=270,y=150)
    view_3 = tk.Radiobutton(window, text='油画版', variable=view_var, value=2)
    view_3.pack()
    view_3.place(x=340,y=150)
    
    print_desk = tk.Text(window, height=6, width=60)
    print_desk.pack()
    print_desk.place(x=40,y=180)
    
    button = tk.Button(window, text='确认', width=5,
                   height=1, command=insert_point)
    button.pack()
    button.place(x=230,y=270)
      
    window.mainloop() 
def main():
    windows =tk.Tk()
    windows.title('My windows')
    windows.geometry('200x200')
    button1=tk.Button(windows, text='Say Hi!', bg='white', width=8,
               height=3,command=windowss)
    button1.pack()
    button1.place(x=70,y=70)
    windows.mainloop()
#if __name__ == '__main__':
 #   main()
 
main()
