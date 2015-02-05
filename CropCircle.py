from SimpleCV import *
import sys

parser = sys.argv
camnumber = int(parser[1])
width = int(parser[2])
height = int(parser[3])

cam = Camera(camnumber, {"width": width, "height": height})
disp = Display()
img = cam.getImage()

down = None
up = None
clr1 = Color.RED
circle = None
bb = None

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
        img.drawLine(down, [disp.mouseX, disp.mouseY], clr1, 2)
    if up is not None and down is not None:
        center = down
        radius = math.sqrt(math.pow(down[0] - up[0],2) + math.pow(down[1] - up[1],2))
        print "Center: " + str(down) + "\tRadius: " + str(radius)
        # topleft = [down[0] - radius, down[1] - radius]
        # bottomright = [down[0] + radius, down[1] + radius]
        # bb = disp.pointsToBoundingBox(topleft,bottomright)
        # print "BB: " + str(bb)
        # img.drawRectangle(bb[0], bb[1], bb[2], bb[3], clr1, 2)
        img.drawCircle(center, radius, clr1, 2)
        circle = Circle(0, center[0], center[1], radius)
    img.save(disp)

# temp = False

while disp.isNotDone():
    img = cam.getImage()
    # crop = bb if temp else circle
    imgCrp = img.crop(circle)
    # if disp.mouseLeft:
        # tempString = "Displaying Circle" if temp else "Displaying Bounding Box"
        # temp = not temp
        # print tempString
    imgCrp.save(disp)

