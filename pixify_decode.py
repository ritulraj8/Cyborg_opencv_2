import numpy as np
import cv2
import os
import sys
import time
import random

'''
Guidelines :- 1) You are not allowed to import libraries other than those already mentioned
              2) You are allowed to code only in the function given below . Code present anywhere else would be ignored by the code verifying exec.
              3) You must code in such a way that the code inside the function is robust for all test cases.
              4) The code verifying exectubale would iterate over the test cases and call this function with one test image at a time. 
'''

def decode(image):
    '''
    Description:- This function takes in image as the input (a numpy array) and returns the character embedded in the image
    For example : if yellow squares = 4 , red squares = 3 , number of shapes containing shapes = 5 . Then the correct character to be returned would be (4*2 + 3*1 + 5) which is p. 
    Note :- if the value comes out to be 32 then the function should return an empty single space " ".
    '''

    ############ Enter your Code Here #################
    character = ""
    img=image
    cropped=img[85:620,80:620]
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    gray=cv2.cvtColor(cropped,cv2.COLOR_BGR2GRAY)
    canny=cv2.Canny(gray,100,200)

    redsquares_no=0
    yellowsquares_no=0
    shapes_no=0

    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    contours,_ = cv2.findContours(mask_yellow,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour)<200:
            yellowsquares_no+=1

    red_lower = np.array([0,120,70])
    red_upper = np.array([10,255,255])
    mask_red1 = cv2.inRange(hsv, red_lower, red_upper)

    red_lower = np.array([170,120,70])
    red_upper = np.array([180,255,255])
    mask_red2 = cv2.inRange(hsv, red_lower, red_upper)

    mask_red = mask_red1 + mask_red2

    contours,_=cv2.findContours(mask_red,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour)<200:
            redsquares_no+=1
    
    ret,r_b_sh_th=cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
    ret,r_b_th=cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
    
    shape=r_b_th-r_b_sh_th
    kernel=np.array(np.ones((int(535/5),int(540/5))))
    stride = (int(535/5),int(540/5))
    for y in range(0, 535, stride[0]):
        for x in range(0,540 , stride[1]):
            patch = shape[y:y + kernel.shape[0], x:x + kernel.shape[1]]
            result = np.sum(patch * kernel)
            if result!=0:
                shapes_no+=1

    value=(1*redsquares_no)+(2*yellowsquares_no)+(1*shapes_no)
    if value==32:
        character+=" "
    else:
        character+=chr(96+value)   
    ###################################################
    return character
    