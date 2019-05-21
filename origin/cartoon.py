# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:25:13 2019

@author: pc
"""

import cv2
num_down = 2#缩减像素采样的数目
num_bilateral = 7#定义双边滤波的数目
#img_rgb = cv2.imread('C:/Users/pc/Desktop/tu/zc.png')
cap = cv2.VideoCapture(0)
ret = True  
while(ret):  
    ret,img_rgb = cap.read()  #按帧读取视频，它的返回值有两个：ret, frame。其中ret是布尔值，如果读取帧是正确的则返回True，如果文件读取到结尾，它的返回值就为False。frame就是每一帧的图像，是个三维矩阵。
    if ret == True:
        img_color = img_rgb
        #高斯金字塔降低取样
        for _ in range(num_down) :
            img_color = cv2.pyrDown(img_color)
            
        #重复使用小的双边滤波代替一个大的滤波
        for _ in range(num_bilateral):
            img_color = cv2.bilateralFilter(img_color,d=9,sigmaColor=9,sigmaSpace=7)
            
        #升采样图片到原始大小
        for _ in range(num_down):
            img_color = cv2.pyrUp(img_color)
            
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.medianBlur(img_gray,7)
        
        #检测到边缘并且增强其效果
        img_edge = cv2.adaptiveThreshold(img_blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY,blockSize=9,C=2)
        
        #转换回彩色图像
        img_edge = cv2.cvtColor(img_edge,cv2.COLOR_GRAY2RGB)
        img_cartoon = cv2.bitwise_and(img_color,img_edge)
        
        cv2.namedWindow("Image")
        cv2.imshow("wty",img_rgb)
        cv2.imshow("Image",img_cartoon)   
        k = cv2.waitKey(20)  #每一帧的播放时间，毫秒级,该参数可以根据显示速率调整
        #如果中途想退出，q键退出，或播放完后，按任意键退出
        if (k & 0xff == ord('q')):  #q键退出!!!!!!!!!
            cap.release()  
            cv2.destroyAllWindows()
            break 
cap.release()  
cv2.waitKey()
cv2.destroyAllWindows()#释放窗口是个好习惯

