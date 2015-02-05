from SimpleCV import *

#Background Image Generator

width = 1280
height = 720
#60-100

i = 0
total = 40 * 1200
totalimg = np.empty((width,height,3))

for s in range(60,100):
    filename = "4hour" + str(s) + ".avi"
    print filename
    video = VirtualCamera(filename,"video")
    img = video.getImage()
    j = 0
    while j < 1200:
        i += 1
        j += 1
        print str(i) + "/" + str(total)
        totalimg += img.getNumpy()
        img = video.getImage()

totalimg = Image(totalimg / i)
totalimg.save("background.png")