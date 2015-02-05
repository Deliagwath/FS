from SimpleCV import *
import sys

parser = sys.argv
width = int(parser[1])
height = int(parser[2])

disp = Display()
cam = Camera(0,{"width":width,"height":height})

normaldisp = True
 
while disp.isNotDone():
 
	if disp.mouseRight:
		normaldisp = not(normaldisp)
		print "Display Mode:", "Normal" if normaldisp else "Segmented" 
	
	img = cam.getImage().flipHorizontal()
	dist = img.colorDistance(SimpleCV.Color.BLACK).dilate(2)
	segmented = dist.stretch(200,255)
	blobs = segmented.findBlobs()
	if blobs:
		circles = blobs.filter([b.isCircle(0.2) for b in blobs])
		if circles:
			img.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),SimpleCV.Color.BLUE,3)
 
	if normaldisp:
		img.show()
	else:
		segmented.show()