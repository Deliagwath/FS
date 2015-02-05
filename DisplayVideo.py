from SimpleCV import *
import sys
import os

parser = sys.argv
vidname = parser[1] #First index is file name
vid = os.path.join('Test_Data',vidname)

video = VirtualCamera(vid,"video")
disp = Display()
while disp.isNotDone():
    if disp.mouseLeft:
        break;
    img = video.getImage()
    img.save(disp)