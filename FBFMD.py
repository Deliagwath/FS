from SimpleCV import *
import sys

class FBFMD():
    
    # __init__ variables
    cam = None
    
    # setArea variables
    clr1 = Color.RED
    clr2 = Color.GREEN
    circle = None
    max_blob_size = None
    min_blob_size = None
    mask = None
    
    def __init__(self):
        parser = sys.argv
        camnumber = int(parser[1])
        width = int(parser[2])
        height = int(parser[3])
        self.cam = Camera(camnumber, {"width":width, "height":height})
    
    def setArea(self):
        disp = Display()
        while disp.isNotDone():
            img = self.cam.getImage()
            if disp.mouseRight:
                break
            if disp.leftButtonDownPosition():
                down = None
                up = None
                down = disp.leftButtonDownPosition()
            if disp.leftButtonUpPosition():
                up = disp.leftButtonUpPosition()
            if down is not None and up is None:
                img.drawLine(down, [disp.mouseX, disp.mouseY], self.clr1, 2)
                radius = math.sqrt(math.pow(down[0] - disp.mouseX, 2) + math.pow(down[1] - disp.mouseY, 2))
                if math.fabs(down[0] - disp.mouseX) > 50 or math.fabs(down[1] - disp.mouseY) > 50:
                    img.drawCircle(down, radius, self.clr1, 2)
            if up is not None and down is not None:
                center = down
                radius = math.sqrt(math.pow(down[0] - up[0], 2) + math.pow(down[1] - up[1], 2))
                print "Center: " + str(down) + "\tRadius: " + str(radius)
                topleft = [down[0] - radius, down[1] - radius]
                bottomright = [down[0] + radius, down[1] + radius]
                bb = disp.pointsToBoundingBox(topleft, bottomright)
                img.drawRectangle(bb[0], bb[1], bb[2], bb[3], self.clr2)
                img.drawCircle(center, radius, self.clr2, 2)
                if circle is None:
                    circle = Circle(0, center[0], center[1], radius)
            img.save(disp)

        croppedDimensions = math.fabs(bottomright[0] - topleft[0]) ** 2
        self.max_blob_size = croppedDimensions * 0.0625  # 1/16
        self.min_blob_size = croppedDimensions * 0.00048828125  # 1/2048

        crpImg = Image(img.size()).crop(self.circle)

        self.mask = Image(crpImg.size())
        dl = DrawingLayer(img.size())
        dl.circle((crpImg.size()[0] / 2, crpImg.size()[1] / 2), crpImg.size()[0] / 2, filled=True, color=Color.WHITE)
        self.mask.addDrawingLayer(dl)
        self.mask = self.mask.applyLayers()
        self.mask = self.mask.invert()
        disp.quit()

    def run(self):
        disp = Display()
        while disp.isNotDone():
            if disp.rightButtonDown:
                print "MRBD Break"
                break
            i = self.cam.getImage()
            if i.size() == (0, 0):
                print "EOF Break"
                break
            im = i.crop(self.circle)
            img = (im - self.mask) + self.mask
            dist = img.colorDistance(Color.WHITE)
            seg = dist.stretch(140, 255).morphOpen().morphOpen()
            blobs = seg.findBlobs(maxsize=self.max_blob_size, minsize=self.min_blob_size)
            if blobs:
                blobs.draw(Color.GREEN,2,False)
                blobs.draw(Color.GREEN,2,False)
            seg.save(disp)