import os
import numpy


path = os.path.dirname(os.path.abspath(__file__))

poscount = 0
oricount = 0
poscountmiss = 0
oricountmiss = 0
sumposdev = 0
sumoridev = 0

posdata = []
oridata = []

for data in os.listdir(os.path.join(path, "data")):
    if data.endswith(".txt"):
        print str(data)
        with open(os.path.join(os.path.join(path, "data"), data), 'r') as opened_file:
            for line in opened_file.readlines():

                if line == "":
                    pass

                elif line[0] == ",":
                    # Orientation
                    angle = float(line[1:])

                    if angle == -1:
                        oricountmiss += 1
                    else:
                        oridata.append(angle)
                        sumoridev += angle
                        oricount += 1

                else:
                    # Position
                    dist = float(line)

                    if dist == -1:
                        poscountmiss += 1
                    else:
                        if dist > 40:
                            continue
                        posdata.append(dist)
                        sumposdev += float(line)
                        poscount += 1

meanposdev = sumposdev / float(poscount)
meanoridev = sumoridev / float(oricount)

posstd = numpy.std(posdata)
oristd = numpy.std(oridata)

print "Mean Position Deviance: " + str(meanposdev)
print "Standard Deviation: " + str(posstd)
print "Data Points Used: " + str(poscount)
print "Data Points Missed: " + str(poscountmiss)
print "Mean Orientation Deviance: " + str(meanoridev)
print "Standard Deviation: " + str(oristd)
print "Data Points Used: " + str(oricount)
print "Data Points Missed: " + str(oricountmiss)

import matplotlib.pyplot as plt

# the histogram of the data
weights = numpy.ones_like(oridata)/len(oridata)
n, bins, patches = plt.hist(oridata, bins=10, facecolor='green', alpha=0.75, weights=weights)

# add a 'best fit' line
# y = mlab.normpdf(bins, meanposdev, posstd)
# l = plt.plot(bins, y, 'r--', linewidth=1)

plt.xlabel('Similarity')
plt.ylabel('Probability (Percentage)')
plt.title('Distribution of Similarity')
# plt.axis([0, 10, 0, 0.2])
plt.grid(True)

plt.show()

print str(oridata)

positivecount = 0
negativecount = 0

for ori in oridata:
    if ori >= 0:
        positivecount += 1
    else:
        negativecount += 1

print positivecount / float(len(oridata))