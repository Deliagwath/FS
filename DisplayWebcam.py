from SimpleCV import *

cam = Camera(0,{"width":1280,"height":720});
disp = Display();
img = cam.getImage();

while disp.isNotDone():
    img = cam.getImage();
    if disp.mouseLeft:
        break;
    if disp.mouseRight:
        img.save("DisplayWebcam.png");
    img.save(disp);