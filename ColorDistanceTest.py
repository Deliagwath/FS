from SimpleCV import *
import NaiveTrackingClass
# import BlobClassification
import os

# Author Pira Limpiti
# Questions or bugs email either
# PPL3000@Gmail.com or
# s1124124@sms.ed.ac.uk

# Program Documentation
# This class, called "CDT" at time of writing

# Is started with 3 variables in __init__()
# Being "live, camno, video"
# live is a boolean denoting whether or not the program is to take in a live feed or not
# If live is true, it draws camno to get the camera number to be used to grab the live feed from
# Else if live is false, it takes in a file name currently hardcoded to a folder in the same directory called Test_Data
# Then the program initiates the live camera or virtual camera via the SimpleCV function Camera() in initCam()

# After the program is initiated, the area needs to be set to reduce computation time and reduce noise
# This is called via setArea(self, circle=None, mask=None)
# There are two ways to call and use this function, one is with no variables, setArea()
# This opens a new SimpleCV display and allows the user to manually draw a circle to denote the area of interest
# The other method is if there is already a saved circle and mask, you can load it into the program without needing to
# manually input by specifying setArea(circle, mask)
# This function MUST be called before nextColorTestFrame() is called because it sets up not only the circle and mask
# required by said function

# The four other set_() functions are to be called outside of this Class to prevent hardcoding of values

# nextColorTestFrame(self, originalImage, track) is the main chunk of the program
# It will take an image from the camera (Which is initialised to either live feed or video)
# Crop the image using the Circle set from setArea()
# Apply the mask also set from setArea()
# Apply Color Distancing, Segmentation, Binarization, Blob Detection
# Then if track is true, then tracks the flies using a naive implementation in the class NaiveTracking.py
# All of the information are then drawn to a Drawing Layer from SimpleCV and then appended to a large Image file to be
# displayed. The output also depends on whether or not originalImage is true, which will either include or exclude
# the unmodified feed

class CDT():

    live = True
    cam = None
    camno = None
    vid = None

    # Variables for reducing computation area
    # Set via setArea(circle, mask)
    # Or set manually with setArea()
    circle = None
    mask = None

    # Blob size will be computed from setArea()
    max_blob_size = None
    min_blob_size = None
    max_blob_multiplier = 0.0625            # 1/16
    min_blob_multiplier = 0.00048828125     # 1/2048

    # Variables for Color Distance Segmentation
    color = [100, 100, 100]
    seglow = 160
    seghigh = 255

    # Variables for Tracking
    trackmin = 1
    trackmax = 30
    tracking = None
    smoothingmethod = None

    # Spatial Variables
    flyprevpos = {1: None, 2: None}
    flyprevori = {1: (None, None), 2: (None, None)}

    # DEBUG Variables
    tolerance = 0.05
    DEBUG = True

    def __init__(self, live, camno, video):
        self.live = live
        self.camno = camno
        self.vid = os.path.join("Test_Data", video)
        self.initCam()

    def initCam(self):
        if self.live:
            self.cam = Camera(self.camno, {"width": 1280, "height": 720})
        else:
            self.cam = VirtualCamera(self.vid, "video")

    def setArea(self, circle=None, mask=None):

        if mask is not None and circle is not None:
            self.circle = circle
            self.mask = mask

            img = self.cam.getImage()
            crpImg = Image(img.size()).crop(self.circle)
            x, y = crpImg.size()
            croppedDimensions = x * y
            self.max_blob_size = croppedDimensions * self.max_blob_multiplier
            self.min_blob_size = croppedDimensions * self.min_blob_multiplier
            self.initCam()
            return

        elif circle is None and mask is not None:
            x, y = mask.size()
            self.circle = Circle(0, x / 2, y / 2, x / 2)

            img = self.cam.getImage()
            crpImg = Image(img.size()).crop(self.circle)
            x, y = crpImg.size()
            croppedDimensions = x * y
            self.max_blob_size = croppedDimensions * self.max_blob_multiplier
            self.min_blob_size = croppedDimensions * self.min_blob_multiplier
            self.initCam()
            return

        elif circle is not None and mask is None:
            self.circle = circle

            img = self.cam.getImage()
            crpImg = Image(img.size()).crop(self.circle)
            x, y = crpImg.size()
            croppedDimensions = x * y
            self.max_blob_size = croppedDimensions * self.max_blob_multiplier
            self.min_blob_size = croppedDimensions * self.min_blob_multiplier
            self.mask = Image(crpImg.size())
            dl = DrawingLayer(img.size())
            dl.circle((crpImg.size()[0] / 2, crpImg.size()[1] / 2), crpImg.size()[0] / 2, filled=True, color=Color.WHITE)
            self.mask.addDrawingLayer(dl)
            self.mask = self.mask.applyLayers()
            self.mask = self.mask.invert()
            self.initCam()
            return

        disp = Display()

        clr1 = Color.RED
        clr2 = Color.GREEN
        down = None
        up = None
        bb = None
        center = None
        radius = None

        while disp.isNotDone():
            img = self.cam.getImage()
            if img.isEmpty():
                self.initCam()
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
                img.drawLine([disp.mouseX, disp.mouseY], down, clr1, 2)
                radius = math.sqrt(math.pow(down[0] - disp.mouseX, 2) + math.pow(down[1] - disp.mouseY, 2))
                if math.fabs(down[0] - disp.mouseX) > 50 or math.fabs(down[1] - disp.mouseY) > 50:
                    img.drawCircle(down, radius, clr1, 2)
            if up is not None and down is not None:
                center = down
                radius = math.sqrt(math.pow(down[0] - up[0], 2) + math.pow(down[1] - up[1], 2))
                # # print "Center: " + str(down) + "\tRadius: " + str(radius)
                topleft = [down[0] - radius, down[1] - radius]
                bottomright = [down[0] + radius, down[1] + radius]
                bb = disp.pointsToBoundingBox(topleft, bottomright)
                img.drawRectangle(bb[0], bb[1], bb[2], bb[3], clr2)
                img.drawCircle(center, radius, clr2, 2)
                if self.circle is None:
                    self.circle = Circle(0, center[0], center[1], radius)
            img.save(disp)

        croppedDimensions = math.fabs(bottomright[0] - topleft[0]) ** 2
        self.max_blob_size = croppedDimensions * self.max_blob_multiplier
        self.min_blob_size = croppedDimensions * self.min_blob_multiplier

        crpImg = Image(img.size()).crop(self.circle)

        self.mask = Image(crpImg.size())
        dl = DrawingLayer(img.size())
        dl.circle((crpImg.size()[0] / 2, crpImg.size()[1] / 2), crpImg.size()[0] / 2, filled=True, color=Color.WHITE)
        self.mask.addDrawingLayer(dl)
        self.mask = self.mask.applyLayers()
        self.mask = self.mask.invert()
        disp.quit()

    def setColor(self, rgb=None):

        if rgb is not None:
            self.color = rgb
            print "Color for segmentation set to: " + str(self.color)
        else:
            self.color = [100, 100, 100]
            print "Color for segmentation set to default: [100, 100, 100]"

    def setSegmentation(self, low=None, high=None):

        if low is not None:
            self.seglow = low
        else:
            self.seglow = 160

        if high is not None:
            self.seghigh = high
        else:
            self.seghigh = 255

        if low is None and high is None:
            print "Segmentation thresholds set to default: min=160 max=255"
        else:
            print "Segmentation thresholds set to: min=" + str(self.seglow) + " max=" + str(self.seghigh)

    def setBlobMultiplier(self, minimum=None, maximum=None):

        # The function may not be very clear
        # The purpose of the multipliers are to scale to the area that is set via the setArea() function
        # Thus a 0.5 minimum would mean no matter what size of an area you pick in the setArea() function is, it will
        # only detect objects that are half the size of the area selected

        if minimum is not None:
            self.min_blob_multiplier = minimum
        else:
            self.min_blob_multiplier = 0.00048828125    # 1/2048

        if maximum is not None:
            self.max_blob_multiplier = maximum
        else:
            self.max_blob_multiplier = 0.0625           # 1/16

        if minimum is None and maximum is None:
            print "Blob Multiplier set to default: min=0.00048828125 max=0.0625"
        else:
            print "Blob Multiplier set to: min=" + str(minimum) + " max=" + str(maximum)

    def setTrackRange(self, minimum=None, maximum=None):

        if minimum is not None:
            self.trackmin = minimum
        else:
            self.trackmin = 1

        if maximum is not None:
            self.trackmax = maximum
        else:
            self.trackmax = 30

        if minimum is None and maximum is None:
            print "Track range thresholds set to default: min=1 max=30"
        else:
            print "Track range thresholds set to: min=" + str(self.trackmin) + " max=" + str(self.trackmax)

    # Valid Smoothing Methods
    # WMA (Weighted Moving Average)
    # None (No Smoothing)
    def setSmoothingMethod(self, method=None, historysize=4):
        self.smoothingmethod = method
        if method == "WMA":
            self.tracking = NaiveTrackingClass.NaiveTrackingClass("WMA", historysize)

    def saveCircle(self, filename):

        # If file exists, remove and create new file
        if os.path.exists(filename):
            os.remove(filename)

        # If circle or mask does not yet exist, send user to manually input circle
        if self.circle is None:
            self.setArea()

        # Creates and writes to new file
        opened_file = open(filename, 'w')

        # Deconstruction of circle for saving
        # Center Co-ordinates and Radius
        x = self.circle.x
        y = self.circle.y
        r = self.circle.radius()

        # Write Co-ordinates
        opened_file.write(str(x) + ',' + str(y) + "\n")

        # Write Radius
        opened_file.write(str(r) + "\n")

        # Close file
        opened_file.close()
        print "Saved Successfully!"

    def loadCircle(self, filename):

        # If file does not exist
        if not os.path.exists(filename):
            print "File does not exist"
            return

        # Else, read from file
        # Reconstruct Circle and set to self.circle
        opened_file = open(filename, 'r')

        data = opened_file.readlines()

        # Parsing position data
        x, y = data[0].strip().split(',')

        # Parsing radius
        r = data[1]

        # Creating Circle Object
        self.circle = Circle(0, int(x), int(y), float(r))

        # Initialising Mask
        self.setArea(self.circle)
        print "Loaded Successfully!"

    def nextColorTestFrame(self, originalImage, track):

        # Check for area initialisation.
        # setArea() is required before this function can run.
        if self.circle is None or self.mask is None:
            print "Area was not initialised, setting area manually."
            self.setArea()

        img1 = self.cam.getImage().crop(self.circle)

        width = img1.width
        height = img1.height

        if originalImage:
            allImg = Image((width * 3, height))
        else:
            allImg = Image((width * 2, height))

        i = self.cam.getImage()
        if i.isEmpty():
            print "End Of File, reinitialize or choose new file"
            return None

        im = i.crop(self.circle)
        img = (im - self.mask) + self.mask
        dist = img.colorDistance(self.color).invert()
        seg = dist.stretch(self.seglow, self.seghigh).morphOpen().binarize(50).invert()
        blobs = seg.findBlobs(minsize=self.min_blob_size, maxsize=self.max_blob_size)

        if originalImage:
            ddl = DrawingLayer((width * 3, height))
            ddl.blit(img, (0, 0))
            ddl.blit(dist, (width, 0))
            ddl.blit(seg, (width * 2, 0))

        else:
            ddl = DrawingLayer((width * 2, height))
            ddl.blit(dist, (0, 0))
            ddl.blit(seg, (width, 0))

        if track:
            data = self.tracking.track(blobs)

            for key in range(1, 3):

                pos1, pos2 = data[key]
                prevpos1, prevpos2 = self.flyprevori[key]

                print "DATA"
                print str(pos1) + "|" + str(pos2)
                print "PREVDATA"
                print str(prevpos1) + "|" + str(prevpos2)

                if pos1 is None:
                    continue

                elif prevpos2 is not None and pos2 is not None:
                    ddl.line(pos1, pos2, Color.RED, 1, False, -1)
                    self.flyprevori[key] = (pos1, pos2)

                elif prevpos2 is not None and pos2 is None:
                    prevori = prevpos2 - prevpos1
                    ddl.line(pos1, pos1 + prevori, Color.ORANGE, 1, False, -1)
                    self.flyprevori[key] = (pos1, pos1 + prevori)

                elif prevpos2 is None and pos2 is not None:
                    ddl.line(pos1, pos2, Color.RED, 1, False, -1)
                    self.flyprevori[key] = (pos1, pos2)

                self.flyprevpos[key] = pos1

        ddl.text(str(self.color), [10, 10], self.color, -1)
        ddl.text('[' + str(self.seglow) + ',' + str(self.seghigh) + ']', [10, 30], self.color, -1)
        allImg.addDrawingLayer(ddl)
        allImg = allImg.applyLayers()
        allBlobs = []
        if blobs:
            for blob in blobs:
                x, y = blob.coordinates()
                allBlobs.append([x, y])
                allBlobs.append([x + width, y])
                if originalImage:
                    allBlobs.append([x + width * 2, y])
        allImg.drawPoints(allBlobs)
        return allImg