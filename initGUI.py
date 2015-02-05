import Tkinter as tK
from ttk import *
import SequentialFBFMD as sF
import os

# GUI Class to help simplify the running of SequentialFBFMD.py

class initGUI(Frame):

    main_program = None

    # Tkinter Variables
    style = None
    ldcheckbox = None
    camlabel = None
    cambox = None
    sourcelabel = None
    sourcebox = None
    trackcheckbox = None
    savefilelabel = None
    savefilebox = None
    loadfilecheckbox = None
    runprogrambutton = None
    quitbutton = None

    # Tkinter Variables for information retrieval
    # Respective to their program variables
    tkld = None
    tktrk = None
    tklf = None

    # Program Variables
    ld = None           # Include original image (Larger Display ld)
    cn = 0              # Camera Number
    live = True         # If the program is live or not
    src = None          # Non live source (Video name)
    trk = False         # Boolean for Tracking
    savefile = "save"  # Save file for saving Circle
    lf = True           # Boolean to check whether or not to save to, or load from file

    def __init__(self, parent):

        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Launch Settings")

        self.style = Style()
        self.style.theme_use("default")
        
        loaded = self.loadlastsession()
        
        self.pack(fill=tK.BOTH, expand=1)

        self.tkld = tK.BooleanVar()
        self.ldcheckbox = tK.Checkbutton\
            (self, text="Include Original Image", variable=self.tkld, onvalue=True, offvalue=False)
        if loaded and self.ld is True:
            self.ldcheckbox.toggle()
        self.ldcheckbox.grid(row=0, column=0)

        self.camlabel = tK.Label(self, text="Camera Number")
        self.camlabel.grid(row=1, column=0)

        self.cambox = tK.Entry(self)
        if loaded:
            self.cambox.insert(0, self.cn)
        else:
            self.cambox.insert(0, "0")
        self.cambox.grid(row=1, column=1)

        self.sourcelabel = tK.Label(self, text="File Name")
        self.sourcelabel.grid(row=2, column=0)

        self.sourcebox = tK.Entry(self)
        if loaded:
            self.sourcebox.insert(0, self.src)
        else:
            self.sourcebox.insert(0, "Leave empty if Live")
        self.sourcebox.grid(row=2, column=1)

        self.tktrk = tK.BooleanVar()
        self.trackcheckbox = tK.Checkbutton\
            (self, text="Include Tracking", variable=self.tktrk, onvalue=True, offvalue=False)
        if loaded and self.trk is True:
            self.trackcheckbox.toggle()
        self.trackcheckbox.grid(row=3, column=0)

        self.savefilelabel = tK.Label(self, text="File name for saving/loading")
        self.savefilelabel.grid(row=4, column=0)

        self.savefilebox = tK.Entry(self)
        if loaded:
            self.savefilebox.insert(0, self.savefile)
        else:
            self.savefilebox.insert(0, "save")
        self.savefilebox.grid(row=4, column=1)

        self.tklf = tK.BooleanVar()
        self.loadfilecheckbox = tK.Checkbutton\
            (self, text="Load from file?", variable=self.tklf, onvalue=True, offvalue=False)
        if loaded and self.lf is True:
            self.loadfilecheckbox.toggle()
        self.loadfilecheckbox.grid(row=5, column=0)

        self.runprogrambutton = tK.Button(self, text="Start", command=self.run)
        self.runprogrambutton.grid(row=6, column=0)

        self.quitbutton = tK.Button(self, text="Quit", command=self.savelastsession)
        self.quitbutton.grid(row=6, column=1)

    def run(self):
        self.ld = self.tkld.get()
        print "Larger Display: " + str(self.ld)
        self.cn = int(self.cambox.get())
        print "Camera Number: " + str(self.cn)
        self.src = self.sourcebox.get()
        disp = "Empty" if self.src == "" else str(self.src)
        print "Video Feed: " + disp
        self.live = True if self.src == "" else False
        print "Live: " + str(self.live)
        self.trk = self.tktrk.get()
        print "Tracking: " + str(self.trk)
        self.savefile = self.savefilebox.get()
        print "Save File Name: " + str(self.savefile)
        self.lf = self.tklf.get()
        print "Load File? " + str(self.lf)
        self.main_program = sF.SequentialFBFMD(True, self.ld, self.cn, self.live, self.src, self.trk, self.savefile, self.lf)

    def savelastsession(self):

        filename = "lastSession"

        # If file exists, remove and create new file
        if os.path.exists(filename):
            os.remove(filename)

        # Creates and writes to new file
        opened_file = open(filename, 'w')

        # Writing arguments to file
        opened_file.write(str(self.tkld.get()).strip() + "\n")
        opened_file.write(str(self.cambox.get()).strip() + "\n")
        opened_file.write(str(self.sourcebox.get()).strip() + "\n")
        opened_file.write(str(self.tktrk.get()).strip() + "\n")
        opened_file.write(str(self.savefilebox.get()).strip() + "\n")
        opened_file.write(str(self.tklf.get()).strip())

        # Close file
        opened_file.close()
        print "Saved Successfully!"
        self.quit()

    # Returns True if there was lastSession information, False otherwise
    def loadlastsession(self):

        filename = "lastSession"

        # If file does not exist
        if not os.path.exists(filename):
            print "File does not exist"
            return False

        # Else, read from file
        opened_file = open(filename, 'r')
        
        try:
            data = opened_file.readlines()

            self.ld = True if data[0].strip() == '1' else False
            self.cn = int(data[1].strip())
            self.src = data[2].strip()
            self.trk = True if data[3].strip() == '1' else False
            self.savefile = data[4].strip()
            self.lf = True if data[5].strip() == '1' else False

        except:
            print "Parsing Failed"
            return False

        print "Loaded Successfully!"
        return True

def main():
    root = tK.Tk()
    app = initGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()