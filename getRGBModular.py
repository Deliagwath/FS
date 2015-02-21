from SimpleCV import *

# Fly Eyes ~(100,50,50)
# Fly Body ~(100,100,100)
# Original intention was to detect the Drosophilia's eyes and bodies
# as two segments and use to get accurate orientation
# However, RED as a segmentation colour does not work when the
# Drosophilia is upside down and cannot be detected as
# clearly in certain circumstances


class GetRGBModular:

    # Variables for instance
    cam = None          # SimpleCV Camera() Object
    live = True         # Get from live feed or file
    extended = None     # Return original feed or not
    vm = None          # ColorDistanceTest instance

    def __init__(self, extended, vm):
        self.extended = extended
        self.vm = vm

    def set_color(self):
        _, _, img = self.vm.next_frame(self.extended, False)

        boolean = False

        disp = Display()
        while disp.isNotDone():

            # Advances one frame via left click
            # Second argument set to false,
            # tracking not necessary to select colour
            # If tracking is on, it can be detrimental as a line
            # is drawn and may interfere with colour selection
            if disp.mouseLeft:
                _, _, img = self.vm.next_frame(self.extended, False)

            # Restarts the feed if arrived at end of file
            if img.isEmpty():
                print "EOF, restarting feed"
                self.vm.init_cam()
                _, _, img = self.vm.next_frame(self.extended, False)

            # Gets colour from pixel currently at mouse position
            # and set segmentation colour
            if disp.mouseRight:
                x = disp.mouseX
                y = disp.mouseY
                pixel = img.getPixel(x, y)
                r, g, b = pixel
                print str(pixel)
                print str(r) + "," + str(g) + "," + str(b)
                boolean = True
                self.vm.set_colour([int(r), int(g), int(b)])
                _, _, img = self.vm.next_frame(self.extended, False)

            # Ends the colour selection process and
            # returns to CDT's next function
            # Press ESC
            # Documentation for usage will be included in program

            if boolean:
                img.drawText("RGB: " + str(r) + "," + str(g) + "," +
                             str(b), x+20, y+20, [int(r), int(g), int(b)], 16)
            img.save(disp)
        disp.quit()

    # Autodetect Circle ranges from
    # 147,169,188
    # 171,208,230
    # Averaging
    # 160,180,200