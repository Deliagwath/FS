from SimpleCV import *
import os
import sys

parser = sys.argv
vidname = parser[1]

vid = os.path.join("Test_Data",vidname)

cam = VirtualCamera(vid, "video")
disp = Display()

down = None
up = None
clr1 = Color.RED
clr2 = Color.GREEN
bb = None
bb1 = None
bb2 = None
curr1 = True

for i in range(0,2):
    img = cam.getImage()

drawimg = img

while disp.isNotDone():
    if disp.mouseMiddle:
        break
    if disp.mouseRight:
        curr1 = not curr1
        print "Creating bb1" if curr1 else "Creating bb2"
    if disp.leftButtonDownPosition():
        down = None
        up = None
        down = disp.leftButtonDownPosition()
    if disp.leftButtonUpPosition():
        up = disp.leftButtonUpPosition()
    if down is not None and up is None:
        bb = disp.pointsToBoundingBox(down,[disp.mouseX, disp.mouseY])
        drawimg.drawRectangle(bb[0],bb[1],bb[2],bb[3],clr1)
    if down is not None and up is not None:
        bb = disp.pointsToBoundingBox(up,down)
        if curr1:
            bb1 = bb
            down = up = None
        else:
            bb2 = bb
            down = up = None
    if bb1 is not None:
        drawimg.drawRectangle(bb1[0],bb1[1],bb1[2],bb1[3])
    if bb2 is not None:
        drawimg.drawRectangle(bb2[0],bb2[1],bb2[2],bb2[3])
    drawimg.save(disp)
    drawimg = img

ts1 = []
ts2 = []
cam = VirtualCamera(vid, "video")
img = cam.getImage()
ts1 = img.track("camshift", ts1, img, bb1)
ts2 = img.track("camshift", ts2, img, bb2)

while disp.isNotDone():
    if disp.mouseRight:
        break
    img = cam.getImage()
    ts1 = img.track("camshift", ts1)
    ts2 = img.track("camshift", ts2)
    ts1.drawBB()
    ts1.drawPath(Color.RED,2)
    ts1.showCoordinates()
    ts2.drawBB()
    ts2.drawPath(Color.GREEN,2)
    ts2.showCoordinates()
    img.save(disp)