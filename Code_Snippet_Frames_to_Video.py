# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 22:44:02 2021

@author: ISHAN
"""

import matplotlib.pyplot as plt
import re
import os
import cv2


image_folder = 'E:/Whatsapp data/whatsapp data/Car Track counter/Output/Out'
video_name = 'video2.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]

images.sort(key=lambda f: int(re.sub('\D', '', f)))
frame = cv2.imread(os.path.join(image_folder, images[0]))

height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 12, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()