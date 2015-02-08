from SimpleCV import *
import NaiveTrackingClass as Ntc
import os

# Author Pira Limpiti
# Questions or bugs, email either
# PPL3000@Gmail.com or
# s1124124@sms.ed.ac.uk

# Program Documentation
# This class, called "CDT" at time of writing

# Is started with 3 variables in __init__()
# Being "live, camno, video"

# live is a boolean denoting whether or not
# the program is to take in a live feed or not

# If live is true, it draws camno to get the camera number
# to be used to grab the live feed from

# Else if live is false, it takes in a file name currently hardcoded
# to a folder in the same directory called Test_Data

# Then the program initiates the live camera or virtual camera
# via the SimpleCV function Camera() in initCam()

# After the program is initiated, the area needs to be set
# to reduce computation time and reduce noise

# This is called via setArea(self, circle=None, mask=None)
# There are two ways to call and use this function,
# one is with no variables, setArea()
# This opens a new SimpleCV display and allows the user to manually
# draw a circle to denote the area of interest

# The other method is if there is already a saved circle and mask,
# you can load it into the program without needing to
# manually input by specifying setArea(circle, mask)
# This function MUST be called before nextColorTestFrame()
# is called because it sets up not only the circle and mask
# required by said function

# The four other set_() functions are to be called
# outside of this Class to prevent hardcoding of values

# nextColorTestFrame(self, originalImage, track)
# is the main chunk of the program
# It will take an image from the camera
# (Which is initialised to either live feed or video)
# Crop the image using the Circle set from setArea()
# Apply the mask also set from setArea()
# Apply Color Distancing, Segmentation, Binarization, Blob Detection
# Then if track is true, then tracks the flies using
# a naive implementation in the class NaiveTracking.py
# All of the information are then drawn to a Drawing Layer
# from SimpleCV and then appended to a large Image file to be
# displayed. The output also depends on whether
# or not originalImage is true, which will either include or exclude
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

    def __init__(self, live, camno, video):
        self.live = live
        self.camno = camno
        self.vid = os.path.join("Test_Data", video)
        self.init_cam()

    def init_cam(self):
        if self.live:
            self.cam = Camera(self.camno, {"width": 1280, "height": 720})
        else:
            self.cam = VirtualCamera(self.vid, "video")

    def set_area(self, circle=None, mask=None):

        # If statements for when arguments are passed into the program
        if mask is not None and circle is not None:
            self.circle = circle
            self.mask = mask

            img = self.cam.getImage()
            cropped_image = Image(img.size()).crop(self.circle)
            x, y = cropped_image.size()
            cropped_dimensions = x * y
            self.max_blob_size = cropped_dimensions * self.max_blob_multiplier
            self.min_blob_size = cropped_dimensions * self.min_blob_multiplier
            self.init_cam()
            return

        elif circle is None and mask is not None:
            x, y = mask.size()
            self.circle = Circle(0, x / 2, y / 2, x / 2)

            img = self.cam.getImage()
            cropped_image = Image(img.size()).crop(self.circle)
            x, y = cropped_image.size()
            cropped_dimensions = x * y
            self.max_blob_size = cropped_dimensions * self.max_blob_multiplier
            self.min_blob_size = cropped_dimensions * self.min_blob_multiplier
            self.init_cam()
            return

        elif circle is not None and mask is None:
            self.circle = circle

            img = self.cam.getImage()
            cropped_image = Image(img.size()).crop(self.circle)
            x, y = cropped_image.size()
            cropped_dimensions = x * y
            self.max_blob_size = cropped_dimensions * self.max_blob_multiplier
            self.min_blob_size = cropped_dimensions * self.min_blob_multiplier
            self.mask = Image(cropped_image.size())
            dl = DrawingLayer(img.size())
            dl.circle((cropped_image.size()[0] / 2,
                       cropped_image.size()[1] / 2),
                      cropped_image.size()[0] / 2,
                      filled=True,
                      color=Color.WHITE)
            self.mask.addDrawingLayer(dl)
            self.mask = self.mask.applyLayers()
            self.mask = self.mask.invert()
            self.init_cam()
            return

        # Code for manual input of area
        disp = Display()

        clr1 = Color.RED
        clr2 = Color.GREEN
        down = None
        up = None
        selected = False

        # Main display loop for choosing area
        while disp.isNotDone():
            img = self.cam.getImage()

            # If feed is from video, reinitialise video if it has ended
            if img.isEmpty():
                self.init_cam()
                img = self.cam.getImage()

            # End area selection
            if disp.mouseRight:
                break

            # Anchor point for midpoint of circle
            if disp.leftButtonDownPosition():
                down = None
                up = None
                down = disp.leftButtonDownPosition()
            if disp.leftButtonUpPosition():
                up = disp.leftButtonUpPosition()

            # Draws what the current area is
            # when mouse button is held down for live feedback
            if down is not None and up is None:
                img.drawLine([disp.mouseX, disp.mouseY], down, clr1, 2)
                radius = math.sqrt(math.pow(down[0] - disp.mouseX, 2)
                                   + math.pow(down[1] - disp.mouseY, 2))
                if math.fabs(down[0] - disp.mouseX) > 50 or \
                        math.fabs(down[1] - disp.mouseY) > 50:
                    img.drawCircle(down, radius, clr1, 2)

            # Show currently selected area
            if up is not None and down is not None:
                center = down
                radius = math.sqrt(math.pow(down[0] - up[0], 2)
                                   + math.pow(down[1] - up[1], 2))
                topleft = [down[0] - radius, down[1] - radius]
                bottomright = [down[0] + radius, down[1] + radius]
                bb = disp.pointsToBoundingBox(topleft, bottomright)
                img.drawRectangle(bb[0], bb[1], bb[2], bb[3], clr2)
                img.drawCircle(center, radius, clr2, 2)
                selected = True
                if self.circle is None:
                    self.circle = Circle(0, center[0], center[1], radius)
            img.save(disp)

        # Just in case if img is not initialised correctly
        # inside loop and breaks through
        img = self.cam.getImage()

        # If a circle was not selected before leaving the loop
        if not selected:
            cropped_dimensions = img.size()[0] * img.size()[1]

        # Calculating min and max blob size according
        # to the new size of computation window
        else:
            cropped_dimensions = math.fabs(bottomright[0] - topleft[0]) ** 2

        self.max_blob_size = cropped_dimensions * self.max_blob_multiplier
        self.min_blob_size = cropped_dimensions * self.min_blob_multiplier

        cropped_image = Image(img.size()).crop(self.circle)

        # Creation of mask for main program loop
        self.mask = Image(cropped_image.size())
        dl = DrawingLayer(img.size())
        dl.circle((cropped_image.size()[0] / 2,
                   cropped_image.size()[1] / 2),
                  cropped_image.size()[0] / 2,
                  filled=True, color=Color.WHITE)
        self.mask.addDrawingLayer(dl)
        self.mask = self.mask.applyLayers()
        self.mask = self.mask.invert()
        disp.quit()

    def set_color(self, rgb=None):

        if rgb is not None:
            self.color = rgb
            print "Color for segmentation set to: " + str(self.color)
        else:
            self.color = [100, 100, 100]
            print "Color for segmentation set \
                  to default: [100, 100, 100]"

    def set_segmentation(self, low=None, high=None):

        if low is not None:
            self.seglow = low
        else:
            self.seglow = 160

        if high is not None:
            self.seghigh = high
        else:
            self.seghigh = 255

        if low is None and high is None:
            print "Segmentation thresholds \
                set to default: min=160 max=255"
        else:
            print "Segmentation thresholds set to: min=" \
                  + str(self.seglow) + " max=" + str(self.seghigh)

    def set_blob_multiplier(self, minimum=None, maximum=None):

        # The function may not be very clear
        # The purpose of the multipliers are to scale to the area
        # that is set via the setArea() function
        # Thus a 0.5 minimum would mean no matter what size of an area
        # you pick in the setArea() function is, it will
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
            print "Blob Multiplier set to default: \
                min=0.00048828125 max=0.0625"
        else:
            print "Blob Multiplier set to: min=" \
                  + str(minimum) + " max=" + str(maximum)

    def set_track_range(self, minimum=None, maximum=None):

        if minimum is not None:
            self.trackmin = minimum
        else:
            self.trackmin = 1

        if maximum is not None:
            self.trackmax = maximum
        else:
            self.trackmax = 30

        if minimum is None and maximum is None:
            print "Track range thresholds \
                set to default: min=1 max=30"
        else:
            print "Track range thresholds set to: min=" \
                  + str(self.trackmin) + " max=" + str(self.trackmax)

    # Valid Smoothing Methods
    # WMA (Weighted Moving Average)
    # None (No Smoothing)
    def set_smoothing_method(self, method=None, historysize=4):
        self.smoothingmethod = method
        if method == "WMA":
            self.tracking = Ntc.NaiveTrackingClass("WMA", historysize)

    def save_circle(self, filename):

        # If file exists, remove and create new file
        if os.path.exists(filename):
            os.remove(filename)

        # If circle or mask does not yet exist,
        # send user to manually input circle
        if self.circle is None:
            self.set_area()

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

    def load_circle(self, filename):

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
        self.set_area(self.circle)
        print "Loaded Successfully!"

    def next_frame(self, original_image, track):

        # Check for area initialisation.
        # setArea() is required before this function can run.
        if self.circle is None or self.mask is None:
            print "Area was not initialised, setting area manually."
            self.set_area()

        img1 = self.cam.getImage().crop(self.circle)

        width = img1.width
        height = img1.height

        # Inclusion of original feed from camera/video
        if original_image:
            all_img = Image((width * 3, height))
        else:
            all_img = Image((width * 2, height))

        # Catch in case something goes wrong with camera initialisation
        i = self.cam.getImage()
        if i.isEmpty():
            print "End Of File, reinitialize or choose new file"
            return None

        # Main vision processing
        im = i.crop(self.circle)

        # Application of mask to reduce computation area
        img = (im - self.mask) + self.mask

        # Finding the color distance from masked image
        dist = img.colorDistance(self.color).invert()

        # Four operations:
        # Segmentation of the color distance image
        # Image morphology using morphOpen (erode then dilate)
        # Binarization of morphed image
        # Inversion of binary image for processing
        seg = dist.stretch(self.seglow, self.seghigh)\
            .morphOpen().binarize(50).invert()

        # Detection of blobs in processed image
        blobs = seg.findBlobs(minsize=self.min_blob_size,
                              maxsize=self.max_blob_size)

        # Creating a Drawing Layer to append and draw data into one image
        if original_image:
            ddl = DrawingLayer((width * 3, height))
            ddl.blit(img, (0, 0))
            ddl.blit(dist, (width, 0))
            ddl.blit(seg, (width * 2, 0))

        else:
            ddl = DrawingLayer((width * 2, height))
            ddl.blit(dist, (0, 0))
            ddl.blit(seg, (width, 0))

        # Main tracking loop for blobs detected
        if track:

            # Sends the detected blobs to the
            # NaiveTrackingClass.py for processing
            # Refer to said class for more information
            data = self.tracking.track(blobs)

            print "Data"
            print "Data1:" + str(data[1])
            print "Data2:" + str(data[2])
            print "-----"

            # Flags to reduce computation if both values were not found
            notfound = {1: False, 2: False}

            # If no data is returned from tracking,
            # attempt to draw previous orientation on new position
            for key in range(1, 3):

                if data[key][0] is None and data[key][1] is None:
                    bulkdata = self.tracking.bulk_track(blobs)

                    pos, boolean = bulkdata[key]
                    prevpos1, prevpos2 = self.flyprevori[key]

                    if pos is None:
                        continue

                    elif prevpos2 is not None and boolean:
                        prevori = prevpos2 - prevpos1
                        ddl.line(pos, pos + prevori,
                                 Color.ORANGE, 1, False, -1)
                        self.flyprevori[key] = (pos, pos + prevori)
                        notfound[key] = True

                    else:
                        continue

            else:

                if notfound[1] and notfound[2]:
                    pass

                else:

                    # key goes through 1 and 2, as identification of flies
                    for key in range(1, 3):

                        pos1, pos2 = data[key]
                        prevpos1, prevpos2 = self.flyprevori[key]

                        # If no data is returned from tracking,
                        # nothing can be drawn
                        if pos1 is None:
                            continue

                        # Draws a line from the data returned from tracking
                        # This will be the orientation of said fly
                        elif prevpos2 is not None and pos2 is not None:
                            ddl.line(pos1, pos2, Color.RED, 1, False, -1)
                            self.flyprevori[key] = (pos1, pos2)

                        # Catch if for first run, as there will be
                        # no previous data, but contains new data
                        elif prevpos2 is None and pos2 is not None:
                            ddl.line(pos1, pos2, Color.RED, 1, False, -1)
                            self.flyprevori[key] = (pos1, pos2)

                        # Sets previous position to new position
                        # for next call of function
                        self.flyprevpos[key] = pos1

        # Displays Color used for Color Distancing
        ddl.text(str(self.color), [10, 10], self.color, -1)

        # Displays values used for segmentation
        ddl.text('[' + str(self.seglow) + ','
                 + str(self.seghigh) + ']', [10, 30], self.color, -1)

        # Drawing all of previous data onto a single image all_img
        all_img.addDrawingLayer(ddl)
        all_img = all_img.applyLayers()
        all_blobs = []

        # Drawing of blobs on all images in all_img, rather than in live image
        if blobs:
            for blob in blobs:
                x, y = blob.coordinates()
                all_blobs.append([x, y])
                all_blobs.append([x + width, y])
                if original_image:
                    all_blobs.append([x + width * 2, y])
        all_img.drawPoints(all_blobs)
        return all_img