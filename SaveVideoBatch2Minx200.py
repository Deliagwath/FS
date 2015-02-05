from SimpleCV import *
import sys

parser = sys.argv
vidname = parser[1] #First index is file name
vidnamedata = vidname.split('.')
width = int(parser[2])
height = int(parser[3])


cam = Camera(0,{"width":width,"height":height})

timetorun = 10 * 120 # 10 Frames for 3 minutes (180 Seconds)
i = 0

for j in range(0,200):
    viditerate = vidnamedata[0] + str(j) + "." + vidnamedata[1]
    vs = VideoStream(viditerate,10,False)
    disp = Display((width,height))
    while disp.isNotDone():
        if i > timetorun:
            break;
        if disp.mouseLeft:
            break;
        img = cam.getImage()
        img.save(vs)
        print str(i) + "/" + str(timetorun)
        img.save(disp)
        i+=1
    print "File " + viditerate + " done!"
    i = 0
        
print "Done!"