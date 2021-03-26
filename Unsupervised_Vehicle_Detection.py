# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 21:11:43 2021

@author: ISHAN
"""


import os 
from os.path import isfile, join 
import re 
import cv2 
import matplotlib.pyplot as plt 
import numpy as np 
import time 


def video_output(frame_folder, name_video ): #Convert frame to video
    
    images = [img for img in os.listdir(frame_folder) if img.endswith(".png")]

    images.sort(key=lambda f: int(re.sub('\D', '', f))) #to sort the frame so that they compile in correct order
    frame = cv2.imread(os.path.join(frame_folder, images[0])) 

    height, width, layers = frame.shape #to get the dimension for the video

    video = cv2.VideoWriter(name_video, 0, 12, (width,height)) #frame rate= 12 fps

    for image in images:
        video.write(cv2.imread(os.path.join(frame_folder, image)))

    cv2.destroyAllWindows()
    video.release()
       
##########################################################################################

def video_process(Input_Loc,pathIn,coord1,coord2):
    
    collected_frames = os.listdir(Input_Loc) #Collecting names of the frame in the folder
    collected_frames.sort(key=lambda f: int(re.sub('\D', '', f))) #To sort them in order 
    collected_images=[] #To collect the images from the folder
    font = cv2.FONT_HERSHEY_DUPLEX #Fonts to write the number of detected vehicles.
    for i in collected_frames: #Iterate over the name of the frames from the folder
        img = cv2.imread(Input_Loc+i) #To read frames
    
        collected_images.append(img) #Adding the frames in the collected_images=[] list
    
        for i in range(len(collected_images)-1):
            
   
            GreyFrameA = cv2.cvtColor(collected_images[i], cv2.COLOR_BGR2GRAY) 
            GreyFrameB = cv2.cvtColor(collected_images[i+1], cv2.COLOR_BGR2GRAY)
            FrameDiffer = cv2.absdiff(GreyFrameB , GreyFrameA )
    
    
            rete, Framethreshold = cv2.threshold(FrameDiffer, 20, 255, cv2.THRESH_BINARY) 
            Framekernel = np.ones((4,4),np.uint8) #Kernal for the dilation.
            Framedilated = cv2.dilate(Framethreshold ,Framekernel,iterations = 1) 


            contour, hierarchies = cv2.findContours(Framedilated.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
            # shortlist contours appearing in the detection zone
            valid_contour = []
    
            for runner in contour:
                x,y,w,h = cv2.boundingRect(runner) #Creates bounding rectangles for the contours
                if (((y-coord1[1])+((coord1[0]-coord2[1])/(coord1[0]-coord2[1]))*(x-coord1[0]))>0) & (cv2.contourArea(runner) >= 400*20): 
                    if (y >= 420) & (cv2.contourArea(runner) < 390): 
                        break
                    valid_contour.append(runner) #Validated contours
    
    
            drawframe = collected_images[i].copy()
            cv2.drawContours(drawframe, valid_contour, -1, (0,0,0), 20)  #Thickness=20
            cv2.line(drawframe, (coord1[0], coord1[1]),(coord2[0],coord2[1]),(0, 0, 0),20)
            cv2.putText(drawframe, "vehicles detected: " + str(len(valid_contour)), (55, 15), font, 0.6, (0, 180, 0), 2)
            cv2.imwrite(pathIn+str(i)+'.png',drawframe )   
    
    """or we can directly manupulate the data and compile the frames into video. Here we first store the frames and later 
    combine them, not recommended for Larger files"""

##########################################################################################

def video_to_frames(location_input, location_output): #Convert Video to frame
    try:
        
        os.mkdir( location_output)
        
    except OSError:
        
        pass
    
    startoftime = time.time() # To get the time taken to complete the process
        
    capture = cv2.VideoCapture(location_input) #Capturing the video feed
    
    vid_length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) - 1 #Number of frame
    print ("Number of frames: ", vid_length) #Print number of frame
    counter = 0
    print ("Converting video..\n") #Print the process
    # Start converting the video
    while capture.isOpened():
       
        rete, frame = capture.read()
        
        cv2.imwrite( location_output + "/%#05d.jpg" % (counter+1), frame)
        counter = counter + 1
        
        if (counter > (vid_length-1)):
           
            endoftime = time.time()
            
            capture.release()
            
            print ("Done extracting frames.\n%d frames extracted" % counter) #Final Results
            print ("It took %d seconds forconversion." % (endoftime- startoftime)) #time taken by the process
            break
            
######################################################################################################

if __name__=="__main__": #Main call to the function

    location_input = '/locIn.mp4' #Enter input location of video data
    location_output = '/locOut' #Enter output location for splitted frames
    output_frames='/loc' #Enter location to save the processed frames
    name_video='Name.avi' #Enter the name for output of the video.
    Coord1=input('enter x1 y1 for crossing line (with space)')
    Coord2=input('enter x2 y2 for crossing line(with space)')
    coord1=Coord1.split()
    coord2=Coord2.split()
    
    video_to_frames(location_input, location_output)
    video_process(location_output,output_frames,coord1,coord2) 
    video_output(output_frames, name_video)