from SimpleCV import *
import sys

parser = sys.argv
vidname = parser[1] #First index is file name
width = int(parser[2])
height = int(parser[3])

vs = VideoStream(vidname,10,False)
cam = Camera(0,{"width":width,"height":height})

disp = Display((width,height))

timetorun = 10 * 120 # 10 Frames for 3 minutes (180 Seconds)
i = 0

while disp.isNotDone():
    if i > timetorun:
        break;
    img = cam.getImage()
    img.save(vs)
    print i + "/" + timetorun
    img.save(disp)
    i+=1

print "Done!"