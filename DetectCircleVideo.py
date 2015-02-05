from SimpleCV import *
import sys
import os

parser = sys.argv
vidname = parser[1]

vid = os.path.join('Test_Data', vidname)

disp = Display()
cam = VirtualCamera(vid, "video")

while disp.isNotDone():
    if disp.mouseRight:
        break
    img = cam.getImage()
    dist = img.colorDistance([160, 180, 200]).invert()
    segmented = dist.stretch(128, 255)
    blobs = segmented.findBlobs()
    if blobs:
        circles = blobs.filter([b.isCircle(0.5) for b in blobs])
        if circles:
            img.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(), Color.BLUE, 3)
	dist.save(disp)