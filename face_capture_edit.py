# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 18:44:23 2019

@author: pc
"""

import dlib                     #人脸识别的库dlib
import numpy as np              #数据处理的库numpy
import cv2                      #图像处理的库OpenCv

def face_init(face_shape_predictor):
    # 使用特征提取器get_frontal_face_detector
    detector = dlib.get_frontal_face_detector()
    # dlib的68点模型，使用作者训练好的特征预测器
    predictor = dlib.shape_predictor(face_shape_predictor)
    
    # 截图screenshoot的计数器
    cnt = 0
    return detector, predictor

def face_capture_e(im_rd,detector, predictor):
    # 眉毛直线拟合数据缓冲
    line_brow_x = []
    line_brow_y = []
    
    # cap.isOpened（） 返回true/false 检查初始化是否成功
    while im_rd is not None:
    
        # 取灰度
        img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)
    
        # 使用人脸检测器检测每一帧图像中的人脸。并返回人脸数rects
        faces = detector(img_gray, 0)
    
        # 待会要显示在屏幕上的字体
        font = cv2.FONT_HERSHEY_SIMPLEX
    
        # 如果检测到人脸
        if len(faces)!=0:
    
            # 对每个人脸都标出68个特征点
            for i in range(len(faces)):
                # enumerate方法同时返回数据对象的索引和数据，k为索引，d为faces中的对象
                for k, d in enumerate(faces):
                    # 用红色矩形框出人脸
                    cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255))#左上右下
                    # 计算人脸框边长
                    face_width = d.right() - d.left()
    
                    # 使用预测器得到68点数据的坐标
                    shape = predictor(im_rd, d)
                    # 圆圈显示每个特征点
                    for i in range(68):
                        cv2.circle(im_rd, (shape.part(i).x, shape.part(i).y), 2, (0, 255, 0), -1, 8)
                        #cv2.putText(im_rd, str(i), (shape.part(i).x, shape.part(i).y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        #            (255, 255, 255))
    
                    # 分析任意n点的位置关系来作为表情识别的依据
                    mouth_width = (shape.part(54).x - shape.part(48).x) / face_width  # 嘴巴咧开程度，宽度
                    mouth_higth = (shape.part(66).y - shape.part(62).y) / face_width  # 嘴巴张开程度，高度
                    # print("嘴巴宽度与识别框宽度之比：",mouth_width_arv)
                    # print("嘴巴高度与识别框高度之比：",mouth_higth_arv)
    
                    # 通过两个眉毛上的10个特征点，分析挑眉程度和皱眉程度
                    brow_sum = 0  # 高度之和
                    frown_sum = 0  # 两边眉毛距离之和
                    for j in range(17, 21):
                        brow_sum += (shape.part(j).y - d.top()) + (shape.part(j + 5).y - d.top())
                        frown_sum += shape.part(j + 5).x - shape.part(j).x
                        line_brow_x.append(shape.part(j).x)
                        line_brow_y.append(shape.part(j).y)
    
                    # self.brow_k, self.brow_d = self.fit_slr(line_brow_x, line_brow_y)  # 计算眉毛的倾斜程度
                    tempx = np.array(line_brow_x)
                    tempy = np.array(line_brow_y)
                    z1 = np.polyfit(tempx, tempy, 1)  # 拟合成一次直线
                    brow_k = -round(z1[0], 3)  # 拟合出曲线的斜率和实际眉毛的倾斜方向是相反的
    
                    brow_hight = (brow_sum / 10) / face_width  # 眉毛高度占比
                    brow_width = (frown_sum / 5) / face_width  # 眉毛距离占比
                    # print("眉毛高度与识别框高度之比：",round(brow_arv/self.face_width,3))
                    # print("眉毛间距与识别框高度之比：",round(frown_arv/self.face_width,3))
    
                    # 眼睛睁开程度
                    eye_sum = (shape.part(41).y - shape.part(37).y + shape.part(40).y - shape.part(38).y +
                               shape.part(47).y - shape.part(43).y + shape.part(46).y - shape.part(44).y)
                    eye_hight = (eye_sum / 4) / face_width
                    # print("眼睛睁开距离与识别框高度之比：",round(eye_open/self.face_width,3))
    
                    # 分情况讨论
                    # 张嘴，可能是开心或者惊讶
                    if round(mouth_higth >= 0.03):
                        if eye_hight >= 0.056:
                            cv2.putText(im_rd, "amazing", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 0, 255), 2, 4)
                        else:
                            cv2.putText(im_rd, "happy", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 0, 255), 2, 4)
    
                    # 没有张嘴，可能是正常和生气
                    else:
                        if brow_k <= -0.3:
                            cv2.putText(im_rd, "angry", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 0, 255), 2, 4)
                        else:
                            cv2.putText(im_rd, "nature", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 0, 255), 2, 4)
    
            # 标出人脸数
            cv2.putText(im_rd, "Faces: "+str(len(faces)), (20,50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            # 没有检测到人脸
            cv2.putText(im_rd, "No Face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
    
        # 添加说明
        im_rd = cv2.putText(im_rd, "Q: quit", (20, 450), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        
        return(im_rd)

if __name__ == '__main__':       
    cap = cv2.VideoCapture(0)
    background = None
    #cap = cv2.VideoCapture("D:/动漫/秒速五厘米/秒速5厘米.mkv")  #指定路径读取视频，如果cv2.VideoCapture（0），没有指定路径，则从电脑自带摄像头取视频。
    ret = True 
    detector, predictor = face_init() 
    #while(cap.isOpened()):  
    while ret:  
        ret,frame = cap.read()  #按帧读取视频，它的返回值有两个：ret, frame。其中ret是布尔值，如果读取帧是正确的则返回True，如果文件读取到结尾，它的返回值就为False。frame就是每一帧的图像，是个三维矩阵。
        if ret == True:
            frame = face_capture_e(frame,detector, predictor)
            cv2.imshow('image', frame)
            #播放视频，第一个参数是视频播放窗口的名称，第二个参数是视频的当前帧。
        k = cv2.waitKey(20)  #每一帧的播放时间，毫秒级,该参数可以根据显示速率调整
        #如果中途想退出，q键退出，或播放完后，按任意键退出
        if (k & 0xff == ord('q')):  #q键退出!!!!!!!!!
            cap.release()  
            cv2.destroyAllWindows()
            break 
    #释放对象和销毁窗口
    cap.release()  
    cv2.waitKey()# 视频结束后，按任意键退出
    cv2.destroyAllWindows()
