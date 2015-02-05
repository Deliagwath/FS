from SimpleCV import *

disp = Display()

img = Image(Image((320,320)).getNumpy() + Color.BLUE)

mask = Image(img.size())
dl = DrawingLayer(img.size())
dl.circle((160,160), 160, filled=True, color=Color.WHITE)
mask.addDrawingLayer(dl)
mask = mask.applyLayers()
masked_image = img - mask.invert()
masked_image = masked_image + mask.invert()

while disp.isNotDone():
    if disp.mouseRight:
        break
    masked_image.save(disp)