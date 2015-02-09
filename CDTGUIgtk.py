from VisionModule import *
import pygtk
pygtk.require('2.0')
import gtk
import gobject


class CDTGUIgtk(gtk.Window):

    # Program Settings (You can change these)
    edge_threshold = 100
    max_scale = 255
    min_scale = 0
    window_width = 500
    window_height = 500
    refresh_rate = 100      # Milliseconds
    live = False            # Whether or not the program takes in a live feed or video feed
    # End Program Settings

    # Variables at runtime
    cdt = None
    current_image = None
    videoname = '4hour55.avi'

    # GUI Variables
    vbox = None
    rScale = None
    gScale = None
    bScale = None

    def __init__(self):

        self.cdt = VisionModule(self.videoname)

        super(CDTGUIgtk, self).__init__()
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("Color Distance Test GUI")
        self.set_decorated(True)
        self.set_has_frame(False)
        self.set_resizable(False)
        self.set_default_size(self.window_width,self.window_height)
        self.connect("destroy", gtk.main_quit)
        self.vbox = gtk.VBox(spacing=4)

        # Setup RGB Scales
        self.rScale = gtk.HScale()
        self.gScale = gtk.HScale()
        self.bScale = gtk.HScale()

        self.rScale.set_range(self.min_scale, self.max_scale)
        self.gScale.set_range(self.min_scale, self.max_scale)
        self.bScale.set_range(self.min_scale, self.max_scale)

        self.rScale.set_size_request(500, 25)
        self.gScale.set_size_request(500, 25)
        self.bScale.set_size_request(500, 25)

        self.rScale.set_value(0)
        self.gScale.set_value(0)
        self.bScale.set_value(0)

        self.rScale.connect("value-changed", self.updateRGB())
        self.gScale.connect("value-changed", self.updateRGB())
        self.bScale.connect("value-changed", self.updateRGB())

        self.vbox.add(self.rScale)
        self.vbox.add(self.gScale)
        self.vbox.add(self.bScale)

        # Setup information labels

        info = gtk.Label()
        info.set_label("Move the sliders to adjust the RGB values")
        self.vbox.add(info)

        self.cdt.set_area()

        # Add the image to the display
        nextImg = self.getNextFrame()
        image = gtk.Image()
        image.set_from_pixbuf(nextImg)
        image.show()
        self.vbox.add(image)

        gobject.timeout_add(self.refresh_rate, self.refresh)
        self.current_image = image
        self.add(self.vbox)
        self.show_all()

    def refresh(self):
        self.updateImage()
        return True

    def getNextFrame(self):
        img = self.cdt.next_frame().getNumpy()
        gtk_img = gtk.gdk.pixbuf_new_from_array(img, gtk.gdk.COLORSPACE_RGB, 8)
        return gtk_img

    def updateImage(self):
        nextImg = self.getNextFrame()
        self.current_image.set_from_pixbuf(nextImg)
        self.show_all()

    def updateRGB(self, scale):

        r = int(self.rScale.get_value())
        g = int(self.gScale.get_value())
        b = int(self.bScale.get_value())
        self.cdt.set_colour([r, g, b])
        print "Color set to: [" + str(r) + ", " + str(g) + ", " + str(b) + "]"


if __name__ == '__main__':
    program = CDTGUIgtk()
    gtk.main()