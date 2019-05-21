# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2

def dodgeV2(image, mask):
    return cv2.divide(image, 255 - mask, scale=256)


def rgb_to_sketch(frame):
    if frame is not None:
        img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # 读取图片时直接转换操作
        # img_gray = cv2.imread('example.jpg', cv2.IMREAD_GRAYSCALE)
        
        img_gray_inv = 255 - img_gray
        img_blur = cv2.GaussianBlur(img_gray_inv, ksize=(21, 21),
                                    sigmaX=0, sigmaY=0)
        img_blend = dodgeV2(img_gray, img_blur)
        
        return(img_blend)