from SimpleCV import *
from VisionModule import *
import sys

# Fly Eyes ~(100,50,50)
# Fly Body ~(100,100,100)

parser = sys.argv
vidname = parser[1]  # First index is file name

disp = Display()
boolean = False

cdt1 = VisionModule(False, 0, vidname)
cdt2 = VisionModule(False, 0, vidname)
cdt3 = VisionModule(False, 0, vidname)

cdt1.init_cam()
cdt2.init_cam()
cdt3.init_cam()
cdt1.set_area()
cdt2.set_area(cdt1.circle)
cdt3.set_area(cdt1.circle)
cdt1.set_segmentation(0, 255)
cdt2.set_segmentation(100, 255)
cdt3.set_segmentation(200, 255)
cdt1.set_colour([100, 100, 100])
cdt2.set_colour([100, 100, 100])
cdt3.set_colour([100, 100, 100])

img = cdt1.next_frame(True, False)
img2 = cdt2.next_frame(True, False)
img3 = cdt3.next_frame(True, False)

width, height = img.size()
allimg = Image((width, height * 3))

ddl = DrawingLayer((width, height * 3))
ddl.blit(img, (0, 0))
ddl.blit(img2, (0, height))
ddl.blit(img3, (0, height * 2))
allimg.addDrawingLayer(ddl)
allimg.applyLayers()

disp = Display()
while disp.isNotDone():
    if disp.mouseLeft:
        img = cdt1.next_frame(True, False)
        img2 = cdt2.next_frame(True, False)
        img3 = cdt3.next_frame(True, False)

        if img.isEmpty() or img2.isEmpty() or img3.isEmpty():
            print "EOF Break"
            break

        ddl = DrawingLayer((width, height * 3))
        ddl.blit(img, (0, 0))
        ddl.blit(img2, (0, height))
        ddl.blit(img3, (0, height * 2))
        allimg.addDrawingLayer(ddl)
        allimg.applyLayers()

    if img.isEmpty():
        print "EOF Break"
        break

    if disp.mouseRight:
        x = disp.mouseX
        y = disp.mouseY

        # Workaround
        pixel = None
        if y < height:
            pixel = img.getPixel(x, y)
        elif height <= y < height * 2:
            pixel = img2.getPixel(x, y - height)
        elif height * 2 <= y < height * 3:
            pixel = img3.getPixel(x, y - height * 2)

        if pixel is None:
            print "Pixel is None: Init to (0,0,0)"
            pixel = (0, 0, 0)

        r, g, b = pixel
        print '[' + str(x) + ',' + str(y) + ']'
        print str(pixel)
        print str(r) + "," + str(g) + "," + str(b)
        boolean = True
        cdt1.set_colour([int(r), int(g), int(b)])
        cdt2.set_colour([int(r), int(g), int(b)])
        cdt3.set_colour([int(r), int(g), int(b)])

    if disp.mouseMiddle:
        print "MMB Break"
        break

    if boolean:
        allimg.drawText("RGB: " + str(r) + "," + str(g) + "," + str(b), x+20, y+20, [int(r), int(g), int(b)], 16)
    allimg.save(disp)

    # Autodetect Circle ranges from
    # 147,169,188
    # 171,208,230
    # Averaging
    # 160,180,200