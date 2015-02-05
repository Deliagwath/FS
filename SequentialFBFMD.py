from SimpleCV import *
import ColorDistanceTest
import getRGBModular
import sys

# Main class program to be run
# This class can either be run from command line with respective variables
# Or run from initGUI.py and recieve arguments from said instance

class SequentialFBFMD():

    # __init__ variables
    ld = False      # Larger Display (LD) {Boolean}
    cn = None       # Camera Number(CN) {Integer}
    live = False    # Live Feed {Boolean}
    src = None      # Source (SRC) {String - Video filename}
    track = False   # Track Objects {Boolean}
    sf = None       # Save File (SF) {String - Save filename}
    lf = None       # Load File (LF) {Boolean}
    cdt = None      # ColorDistanceTest (CDT) {Main Vision Class}
    cam = None      # Camera (CAM) {SimpleCV Camera() Object}

    def __init__(self, gui=False, ld=None, cn=None, live=None, src=None, trk=None, sf=None, lf=None):

        # If not running from GUI, run cmdInit() which takes arguments from command line
        if not gui:
            self.cmdInit()
            return

        self.ld = ld
        self.cn = cn
        self.live = live
        self.src = src
        self.track = trk
        self.sf = sf
        self.lf = lf

        self.startProgram()

    def cmdInit(self):

        # Parsing inputs
        parser = sys.argv

        # Parsing inputs to correct data type

        self.ld = True if parser[1] == 'True' else False
        self.cn = int(parser[2])
        self.live = True if parser[3] == 'True' else False
        self.src = parser[4]
        self.track = True if parser[5] == 'True' else False
        self.sf = parser[6]
        self.lf = True if parser[7] == 'True' else False

        self.startProgram()

    # Modifications to sequence of program should be modified in here
    # This is where all of the main ColorDistanceTest functions are called
    def startProgram(self):
        # Initialising Program
        self.cdt = ColorDistanceTest.CDT(self.live, self.cn, self.src)
        if load:
            self.cdt.loadCircle(self.sf)
        else:
            self.cdt.setArea()
            self.cdt.saveCircle(self.sf)

        # Set custom values here rather than hardcoding in ColorDistanceTest.py
        self.cdt.setSegmentation()
        self.cdt.setBlobMultiplier()
        self.cdt.setTrackRange()
        # So far, only one smoothing method was implemented, being WMA
        # Otherwise, pass None or nothing at all to not apply smoothing
        self.cdt.setSmoothingMethod("WMA")
        # self.cdt.setColor() # If ran without arguments, sets the color to [100, 100, 100] overriding setDistColor()

        self.setDistColor()

        self.run()

    def setDistColor(self):
        getRGB = getRGBModular.getRGBModular(self.ld, self.cdt)
        getRGB.setColor()
        # No need to call self.cdt to set color, it is set inside getRGBModular's class

    # Run gets the next frame every time you left click
    # Continuously runs when middle clicked (Toggle)
    # Stops the program when right clicked
    def run(self):
        disp = Display()

        img = self.cdt.nextColorTestFrame(self.ld, self.track)

        continuous = False

        while disp.isNotDone():

            if continuous:
                img = self.cdt.nextColorTestFrame(self.ld, self.track)

            if disp.mouseMiddle:
                print "MMB"
                continuous = not continuous

            if disp.mouseLeft:
                print "LMB"
                img = self.cdt.nextColorTestFrame(self.ld, self.track)

            if disp.mouseRight:
                print "MRB"
                break

            if img.isEmpty():
                print "EOF"
                break

            img.save(disp)
        disp.quit()

if __name__ == '__main__':
    app = SequentialFBFMD()