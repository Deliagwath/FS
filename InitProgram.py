from SimpleCV import *
import VisionModule
import GetRGBModular
import SaveVideo
import sys

# Main class program to be run
# This class can either be run from command line
# with respective variables or run from initGUI.py
# and recieve arguments from said instance


class InitProgram():

    # __init__ variables
    ld = False      # Larger Display (LD) {Boolean}
    cn = None       # Camera Number(CN) {Integer}
    live = False    # Live Feed {Boolean}
    src = None      # Source (SRC) {String - Video filename}
    track = False   # Track Objects {Boolean}
    sf = None       # Save File (SF) {String - Save filename}
    lf = None       # Load File (LF) {Boolean}
    vm = None       # Vision Module (VM) {Main Vision Class}
    sv = None       # Recording Class (SV) [Save Video Class]
    vn = None       # Video Name (VN) [String - Filename to save to]
    cam = None      # Camera (CAM) {SimpleCV Camera() Object}

    def __init__(self, gui=False, ld=None, cn=None,
                 live=None, src=None, trk=None, sf=None,
                 lf=None, vn=None):

        # If not running from GUI, run cmdInit()
        # which takes arguments from command line
        if not gui:
            self.cmd_init()
            return

        self.ld = ld
        self.cn = cn
        self.live = live
        self.src = src
        self.track = trk
        self.sf = sf
        self.lf = lf
        self.vn = vn

        self.start_program()

    def cmd_init(self):

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
        self.vn = parser[8]

        self.start_program()

    # Modifications to sequence of program should be modified in here
    # This is where all of the main ColorDistanceTest functions are called
    def start_program(self):
        # Initialising Program
        self.vm = VisionModule.VisionModule(self.live, self.cn, self.src)
        if load:
            self.vm.load_circle(self.sf)
        else:
            self.vm.set_area()
            self.vm.save_circle(self.sf)

        # Set custom values here rather
        # than hardcoding in VisionModule.py
        self.vm.set_segmentation()
        self.vm.set_blob_multiplier()
        self.vm.set_track_range()
        # So far, only one smoothing method was implemented, being WMA
        # Otherwise, pass None or nothing at all to not apply smoothing
        self.vm.set_smoothing_method("WMA")
        # self.cdt.setColor() # If ran without arguments,
        # sets the color to [100, 100, 100] overriding setDistColor()

        self.set_dist_color()

        self.run()

    def set_dist_color(self):
        get_colour = GetRGBModular.GetRGBModular(self.ld, self.vm)
        get_colour.set_color()
        # No need to call self.cdt to set color,
        # it is set inside getRGBModular's class

    # Run gets the next frame every time you left click
    # Continuously runs when middle clicked (Toggle)
    # Stops the program when right clicked
    def run(self):
        disp = Display()

        original, data, img = self.vm.next_frame(self.ld, self.track)

        continuous = False
        lastimg = None
        end = False

        while disp.isNotDone():

            if continuous:
                original, data, img = self.vm.next_frame(self.ld, self.track)
                if original is None and data is None and img is None:
                    end = True
                    img = lastimg

            if end is True:
                continuous = False
                if self.sv is not None:
                    self.sv.end()
                    self.sv = None

            if self.sv is not None and continuous:
                self.sv.record(original, data)

            if disp.leftButtonDown:
                print "Toggled Continuous"
                continuous = not continuous

            if disp.mouseWheelDown:
                original, data, img = self.vm.next_frame(self.ld, self.track)

            if disp.rightButtonDown:
                # Record
                if self.sv is None and end is False:
                    self.sv = SaveVideo.SaveVideo(self.vn)
                    print "Recording to " + self.sv.vidname
                elif end is False:
                    print "Saving to " + self.sv.vidname
                    self.sv.end()
                    print "Ending recording"
                    self.sv = None
                else:
                    print "Cannot record from End of File"

            if img.isEmpty():
                print "EOF"
                break

            if self.sv is not None:
                width, height = img.size()
                ddl = DrawingLayer((width, height))
                ddl.circle((20, height - 20), 5,
                           Color.RED, 1, True, -1, False)
                img.addDrawingLayer(ddl)
                img.applyLayers()

            img.save(disp)
            lastimg = img
        disp.quit()

if __name__ == '__main__':
    app = InitProgram()