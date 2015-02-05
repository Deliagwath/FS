from SimpleCV import *
import sys

class SaveVideo:

    def main(self):
        parser = sys.argv
        vidname = parser[1] #First index is file name
        width = int(parser[2])
        height = int(parser[3])
        
        vs = VideoStream(vidname,10,False)
        cam = Camera(0,{"width":width,"height":height})
        
        disp = Display((width,height))
        
        while disp.isNotDone():
            if disp.mouseLeft:
                break;
            img = cam.getImage()
            img.save(vs)
            img.save(disp)

if __name__ == "__main__":
    SV = SaveVideo()
    SV.main()