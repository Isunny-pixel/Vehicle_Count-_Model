# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 16:48:00 2021

@author: ISHAN
"""


from os.path import isfile, join
import re
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np


# get file names of the frames
col_frames = os.listdir('E:/Whatsapp data/whatsapp data/Car Track counter/DATA/Frame/')

# sort file names
col_frames.sort(key=lambda f: int(re.sub('\D', '', f)))

# empty list to store the frames
    col_images=[]

for i in col_frames:
    # read the frames
    img = cv2.imread('E:/Whatsapp data/whatsapp data/Car Track counter/DATA/Frame/'+i)
    # append the frames to the list
    col_images.append(img)
    
# kernel for image dilation
kernel = np.ones((4,4),np.uint8)

# font style
font = cv2.FONT_HERSHEY_SIMPLEX



"""
# specify video name
pathOut = 'vehicle_detection_v4.mp4'

# specify frames per second
fps = 30.0

frame_array = []
files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]

files.sort(key=lambda f: int(re.sub('\D', '', f)))

for i in range(len(files)):
    filename=pathIn + files[i]
    
    #read frames
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    
    #inserting the frames into an image array
    frame_array.append(img)
size = img[0].shape[1], img[0].shape[0]
out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

for i in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[i])

out.release('E:/Whatsapp data/whatsapp data/Car Track counter/Output/Out/')
"""