from SimpleCV import *
import sys
import os

# Fly Eyes ~(100,50,50)
# Fly Body ~(100,100,100)

parser = sys.argv
vidname = parser[1]  # First index is file name

vid = os.path.join('Test_Data', vidname)

cam = VirtualCamera(vid, "video")
disp = Display()
boolean = False

img = cam.getImage()

while disp.isNotDone():
    if disp.mouseLeft:
        img = cam.getImage()
    if img.isEmpty():
        print "EOF Break"
        break
    # im = i.crop(circle)
    # img = (im - mask) + mask
    if disp.mouseRight:
        x = disp.mouseX
        y = disp.mouseY
        pixel = img.getPixel(x,y)
        r, g, b = pixel
        print str(pixel)
        print str(r) + "," + str(g) + "," + str(b)
        boolean = True

    if disp.mouseMiddle:
        print "MMB Break"
        break

    if boolean:
        img.drawText("RGB: " + str(r) + "," + str(g) + "," + str(b), x+20, y+20, [int(r), int(g), int(b)], 16)
    img.save(disp)

    # Autodetect Circle ranges from
    # 147,169,188
    # 171,208,230
    # Averaging
    # 160,180,200