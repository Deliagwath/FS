from math import sqrt
# Implementing Smoothing algorithms to remove or reduce the effect of noise on vision processing
# Takes in positions calculated by NaiveTracking passed though ColorDistanceTest to return an averaged orientation

class Smoothing():

    positions = None
    orientations = None
    percentages = None
    queuesize = 0

    def __init__(self, smoothingTechnique, queuesize=3):

        if smoothingTechnique == "WeightedMovingAverage":
            self.positions = []
            self.orientations = []
            self.initWeights(queuesize)
            self.queuesize = queuesize
        else:
            print "Unknown Smoothing Technique"

    def weightedMovingAverage(self, newpos):

        if len(self.positions) == self.queuesize:
            self.positions.pop(0)

        self.positions.append(newpos)
        self.recalculateOrientations()

        if len(self.orientations) == 0:
            return None
        elif len(self.orientations) == 1:
            return self.orientations[0]

        total = [0, 0]
        for index, ori in enumerate(self.orientations):
            total[0] += self.percentages[index] * ori[0]
            total[1] += self.percentages[index] * ori[1]

        orientation = [total[0] / self.queuesize, total[1] / self.queuesize]
        magnitude = sqrt((orientation[0] ** 2) + (orientation ** 2))
        return [orientation[0] / magnitude, orientation[1] / magnitude]

    def recalculateOrientations(self):

        if len(self.positions) <= 1:
            return None

        prevx, prevy = self.positions[self.queuesize - 2]
        currx, curry = self.positions[self.queuesize - 1]

        diffx = currx - prevx
        diffy = curry - prevy

        magnitude = sqrt((diffx ** 2) + (diffy ** 2))

        orientation = [diffx / magnitude, diffy / magnitude]

        if self.orientations == self.queuesize - 1:
            self.orientations.pop(0)

        self.orientations.append(orientation)

    def initWeights(self, size):

        total = 0

        for i in range(1, size + 1):
            total += i

        self.percentages = []
        for i in range(1, size + 1):
            self.percentages.append(i / float(total))