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
bool = False

# down = None
# up = None
# clr1 = Color.RED
# clr2 = Color.GREEN
# bb = None
# circle = None
# center = None
# radius = None
#
# while disp.isNotDone():
#     img = cam.getImage()
#     if disp.mouseRight:
#         break
#     if disp.leftButtonDownPosition():
#         down = None
#         up = None
#         down = disp.leftButtonDownPosition()
#     if disp.leftButtonUpPosition():
#         up = disp.leftButtonUpPosition()
#     if down is not None and up is None:
#         img.drawLine([disp.mouseX, disp.mouseY], down, clr1, 2)
#         radius = math.sqrt(math.pow(down[0] - disp.mouseX, 2) + math.pow(down[1] - disp.mouseY, 2))
#         if math.fabs(down[0] - disp.mouseX) > 50 or math.fabs(down[1] - disp.mouseY) > 50:
#             img.drawCircle(down, radius, clr1, 2)
#     if up is not None and down is not None:
#         center = down
#         radius = math.sqrt(math.pow(down[0] - up[0], 2) + math.pow(down[1] - up[1], 2))
#         # print "Center: " + str(down) + "\tRadius: " + str(radius)
#         topleft = [down[0] - radius, down[1] - radius]
#         bottomright = [down[0] + radius, down[1] + radius]
#         bb = disp.pointsToBoundingBox(topleft, bottomright)
#         img.drawRectangle(bb[0], bb[1], bb[2], bb[3], clr2)
#         img.drawCircle(center, radius, clr2, 2)
#         if circle is None:
#             circle = Circle(0, center[0], center[1], radius)
#     img.save(disp)
#
# cam = VirtualCamera(vid, "video")
#
# img1 = cam.getImage().crop(circle)
#
# mask = Image(img1.size())
# dl = DrawingLayer(img1.size())
# dl.circle((img1.size()[0]/2,img1.size()[1]/2), img1.size()[0]/2, filled=True, color=Color.WHITE)
# mask.addDrawingLayer(dl)
# mask = mask.applyLayers()
# mask = mask.invert()

while disp.isNotDone():
    img = cam.getImage()
    if img.isEmpty():
        print "EOF Break"
        break
    # im = i.crop(circle)
    # img = (im - mask) + mask
    if disp.mouseLeft:
        x = disp.mouseX
        y = disp.mouseY
        pixel = img.getPixel(x,y)
        r, g, b = pixel
        print str(pixel)
        print str(r) + "," + str(g) + "," + str(b)
        bool = True

    if disp.mouseMiddle:
        print "MMB Break"
        break

    if bool:
        img.drawText("RGB: " + str(r) + "," + str(g) + "," + str(b),x+20,y+20,[int(r),int(g),int(b)],16)
    img.save(disp)

    # Autodetect Circle ranges from
    # 147,169,188
    # 171,208,230
    # Averaging
    # 160,180,200