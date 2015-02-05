from sys import maxsize
from SimpleCV import *
import sys
import os

parser = sys.argv
vidname = parser[1]  # First index is file name

vid = os.path.join('Test_Data', vidname)

cam = VirtualCamera(vid, "video")
disp = Display()

down = None
up = None
clr1 = Color.RED
clr2 = Color.GREEN
bb = None
circle = None
center = None
radius = None

while disp.isNotDone():
    img = cam.getImage()
    if disp.mouseRight:
        break
    if disp.leftButtonDownPosition():
        down = None
        up = None
        down = disp.leftButtonDownPosition()
    if disp.leftButtonUpPosition():
        up = disp.leftButtonUpPosition()
    if down is not None and up is None:
        img.drawLine([disp.mouseX, disp.mouseY], down, clr1, 2)
        radius = math.sqrt(math.pow(down[0] - disp.mouseX, 2) + math.pow(down[1] - disp.mouseY, 2))
        if math.fabs(down[0] - disp.mouseX) > 50 or math.fabs(down[1] - disp.mouseY) > 50:
            img.drawCircle(down, radius, clr1, 2)
    if up is not None and down is not None:
        center = down
        radius = math.sqrt(math.pow(down[0] - up[0], 2) + math.pow(down[1] - up[1], 2))
        # print "Center: " + str(down) + "\tRadius: " + str(radius)
        topleft = [down[0] - radius, down[1] - radius]
        bottomright = [down[0] + radius, down[1] + radius]
        bb = disp.pointsToBoundingBox(topleft, bottomright)
        img.drawRectangle(bb[0], bb[1], bb[2], bb[3], clr2)
        img.drawCircle(center, radius, clr2, 2)
        if circle is None:
            circle = Circle(0, center[0], center[1], radius)
    img.save(disp)

cam = VirtualCamera(vid, "video")

croppedDimensions = math.fabs(bottomright[0] - topleft[0]) ** 2

max_blob_size = croppedDimensions * 0.0625           # 1/16
min_blob_size = croppedDimensions * 0.00048828125   # 1/2048

img1 = cam.getImage().crop(circle)

mask = Image(img1.size())
dl = DrawingLayer(img1.size())
dl.circle((img1.size()[0]/2,img1.size()[1]/2), img1.size()[0]/2, filled=True, color=Color.WHITE)
mask.addDrawingLayer(dl)
mask = mask.applyLayers()
mask = mask.invert()

width = img1.width
height = img1.height

allImg = Image((width*3,height))

curr1 = True
bb1 = None
bb2 = None

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
        img1.drawRectangle(bb[0],bb[1],bb[2],bb[3],clr1)
    if down is not None and up is not None:
        bb = disp.pointsToBoundingBox(up,down)
        if curr1:
            bb1 = bb
            down = up = None
        else:
            bb2 = bb
            down = up = None
    if bb1 is not None:
        img1.drawRectangle(bb1[0],bb1[1],bb1[2],bb1[3])
    if bb2 is not None:
        img1.drawRectangle(bb2[0],bb2[1],bb2[2],bb2[3])
    img1.save(disp)

img1 = (img1 - mask) + mask
dist1 = img1.colorDistance([100,50,50]).invert()
seg1 = dist1.stretch(128,255).morphOpen()

ts1 = []
ts1 = seg1.track("CAMSHIFT",ts1,seg1,bb1,3)
ts2 = []
ts2 = seg1.track("CAMSHIFT",ts2,seg1,bb2,3)

while disp.isNotDone():
    if disp.rightButtonDown:
        print "MRBD Break"
        break
    i = cam.getImage()
    if i.isEmpty():
        print "EOF Break"
        break
    im = i.crop(circle)
    img = (im - mask) + mask
    dist = img.colorDistance([100,50,50]).invert()
    seg = dist.stretch(128,255).morphOpen()
    ts1 = seg.track("CAMSHIFT",ts1)
    ts2 = seg.track("CAMSHIFT",ts2)
    blobs = seg.findBlobs(minsize=min_blob_size,maxsize=max_blob_size)
    if blobs:
        blobs.draw()
    ddl = DrawingLayer((width*3,height))
    ddl.blit(img)
    ddl.blit(dist,(width,0))
    ddl.blit(seg,(width*2,0))
    allImg.addDrawingLayer(ddl)
    allImg = allImg.applyLayers()
    allBlobs = []
    for blob in blobs:
        x,y = blob.coordinates()
        allBlobs.append([x,y])
        allBlobs.append([x+width,y])
        allBlobs.append([x+width*2,y])
    blobs = allImg.findBlobs(minsize=min_blob_size,maxsize=max_blob_size)
    if blobs:
        blobs.draw()
    allImg.drawPoints(allBlobs)
    ts1.drawPath()
    ts2.drawPath()
    allImg.save(disp)
    if disp.mouseLeft:
        allImg.save("Detect.png")
        print "Saved to Detect.png"