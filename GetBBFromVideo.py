from SimpleCV import *
import sys

parser = sys.argv
vidname = parser[1] #First index is file name

video = VirtualCamera(vidname,"video")
disp = Display()

down = None
up = None

clr1 = (255,0,0)
clr2 = (0,255,0)

while(disp.isNotDone()):
    img = video.getImage()
    if (disp.leftButtonDownPosition()):
        down = disp.leftButtonDownPosition()
    if (disp.leftButtonUpPosition()):
        up = disp.leftButtonUpPosition()
    if (up is not None and down is not None):
        print str(up) + " " + str(down)
        bb1 = disp.pointsToBoundingBox(up,down)
        img.drawRectangle(bb1[0],bb1[1],bb1[2],bb1[3],clr1)
        break;
    img.save(disp)

down = None
up = None

while(disp.isNotDone()):
    img = video.getImage()
    img.drawRectangle(bb1[0],bb1[1],bb1[2],bb1[3],clr1)
    if (disp.leftButtonDownPosition()):
        down = disp.leftButtonDownPosition()
    if (disp.leftButtonUpPosition()):
        up = disp.leftButtonUpPosition()
    if (up is not None and down is not None):
        print str(up) + " " + str(down)
        bb2 = disp.pointsToBoundingBox(up,down)
        img.drawRectangle(bb1[0],bb1[1],bb1[2],bb1[3],clr1)
        img.drawRectangle(bb2[0],bb2[1],bb2[2],bb2[3],clr2)
    img.save(disp)

while(disp.isNotDone()):
    img = video.getImage()
    img.save(disp)
    if (disp.mouseLeft):
        break;

print "Bounding Box Red: (" + str(bb1[0]) + "," + str(bb1[1]) + "," + str(bb1[2]) + "," + str(bb1[3]) + ")"
print "Bounding Box Green: (" + str(bb2[0]) + "," + str(bb2[1]) + "," + str(bb2[2]) + "," + str(bb2[3]) + ")"