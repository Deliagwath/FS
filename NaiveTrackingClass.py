from math import sqrt

class NaiveTrackingClass:

    smoothingmethod = None
    weights = None
    fly1past = None
    fly1pastori = None
    fly2past = None
    fly2pastori = None
    size = 4
    minrange = 1
    maxrange = 30

    def __init__(self, smoothing=None, size=4):

        self.fly1past = []
        self.fly2past = []

        if smoothing is "WMA":
            self.smoothingmethod = smoothing
            self.size = size
            self.fly1pastori = []
            self.fly2pastori = []
            self.initWeights()
            self.initArrays()
        else:
            self.size = 1

    def initArrays(self):

        for i in range(0, self.size):
            self.fly1past.append(None)
            self.fly2past.append(None)

        for i in range(0, self.size - 1):
            self.fly1pastori.append(None)
            self.fly2pastori.append(None)

    def initWeights(self):

        total = 0

        for i in range(1, self.size + 1):
            total += i

        self.weights = []
        for i in range(1, self.size + 1):
            self.weights.append(i / float(total))

    def withinRange(self, flyno, pos):

        # Retrieving past data for calculation
        if flyno == 1:
            deltax = pos[0] - self.fly1past[-1][0]
            deltay = pos[1] - self.fly1past[-1][1]

        elif flyno == 2:
            deltax = pos[0] - self.fly2past[-1][0]
            deltay = pos[1] - self.fly2past[-1][1]

        else:
            print "Incorrect Arguments: Line 63 NaiveTrackingClass.py"
            return False, None

        # Calculating magnitude of difference between two points to attempt to retain identity
        magnitude = sqrt((deltax ** 2) + (deltay ** 2))

        if self.minrange < magnitude < self.maxrange:
            orientation = [(deltax / magnitude) * 1000, (deltay / magnitude) * 1000]
            return magnitude, orientation
        else:
            return False, None

    def setRange(self, minrange=None, maxrange=None):
        if minrange is None and maxrange is None:
            self.minrange = 1
            self.maxrange = 30
        if minrange is not None:
            self.minrange = minrange
        if maxrange is not None:
            self.maxrange = maxrange

    def addPosition(self, pos1=None, pos2=None):

        # Populating array [Fly #1]
        if len(self.fly1past) == self.size and pos1 is not None:
            self.fly1past.pop(0)
            self.fly1past.append(pos1)

        elif pos1 is not None:
            self.fly1past.append(pos1)

        else:
            pass

        # Populating array [Fly #2]
        if len(self.fly2past) == self.size and pos2 is not None:
            self.fly2past.pop(0)
            self.fly2past.append(pos2)

        elif pos2 is not None:
            self.fly2past.append(pos2)

        else:
            pass

    def replacePosition(self, pos1=None, pos2=None):

        if pos1 is not None:
            self.fly1past[-1] = pos1

        if pos2 is not None:
            self.fly2past[-1] = pos2

    def addOrientation(self, ori1=None, ori2=None):

        # Populating array [Fly #1 Orientation]
        if len(self.fly1pastori) == (self.size - 1) and ori1 is not None:
            self.fly1pastori.pop(0)
            self.fly1pastori.append(ori1)

        elif ori1 is not None:
            self.fly1pastori.append(ori1)

        else:
            pass

        # Populating array [Fly #2 Orientation]
        if len(self.fly2pastori) == (self.size - 1) and ori2 is not None:
            self.fly2pastori.pop(0)
            self.fly2pastori.append(ori2)

        elif ori2 is not None:
            self.fly2pastori.append(ori2)

        else:
            pass

    def replaceOrientation(self, ori1=None, ori2=None):

        if ori1 is not None:
            self.fly1pastori[-1] = ori1

        if ori2 is not None:
            self.fly2pastori[-1] = ori2

    # Used for WMA (Weighted Moving Average) calculation
    # Takes previous orientations to calculate an average of where the orientation should be
    def calculateOrientation(self):

        sum1 = [0, 0]
        sum2 = [0, 0]

        for index, ori in enumerate(self.fly1pastori):
            if ori is None:
                continue
            sum1[0] += self.weights[index] * ori[0]
            sum1[1] += self.weights[index] * ori[1]

        for index, ori in enumerate(self.fly2pastori):
            if ori is None:
                continue
            sum2[0] += self.weights[index] * ori[0]
            sum2[1] += self.weights[index] * ori[1]

        ori1 = [sum1[0] / float(self.size - 1), sum1[1] / float(self.size - 1)]
        ori2 = [sum2[0] / float(self.size - 1), sum2[1] / float(self.size - 1)]

        if self.fly1pastori[-1] is None:
            ori1 = None
        if self.fly2pastori[-1] is None:
            ori2 = None

        return ori1, ori2

    # Returns a dictionary with the fly id as the key, and two co-ordinates ((x,y), (x2,y2)) as values.
    def track(self, blobs):

        returndict = {}
        mag1 = 0
        mag2 = 0

        init1 = False
        init2 = False

        first = True

        for pos in blobs.coordinates():

            if self.fly1past[-1] is None:
                self.addPosition(pos1=pos)
                returndict[1] = (pos, None)
                init1 = True
                continue

            if self.fly2past[-1] is None:
                self.addPosition(pos2=pos)
                returndict[2] = (pos, None)
                init2 = True
                continue

            if init1 and init2:
                break

            # Checks if the new co-ordinates are within range of the new co-ordinate
            if not init1:
                magnitude1, orientation1 = self.withinRange(1, pos)

            if not init2:
                magnitude2, orientation2 = self.withinRange(2, pos)

            # If smoothingmethod is Weighted Moving Average ("WMA")
            if self.smoothingmethod == "WMA":
                if first:
                    self.addOrientation(orientation1, orientation2)
                    first = False
                else:
                    self.replaceOrientation(orientation1, orientation2)

                self.calculateOrientation()
                ori1, ori2 = self.calculateOrientation()

                if not init1 and magnitude1 and 1 not in returndict:
                    returndict[1] = (pos, (pos[0] + ori1[0], pos[1] + ori1[1]))
                    mag1 = magnitude1
                    self.addPosition(pos1=pos)

                elif not init1 and magnitude1 and 1 in returndict and magnitude1 < mag1:
                    returndict[1] = (pos, (pos[0] + ori1[0], pos[1] + ori1[1]))
                    mag1 = magnitude1
                    self.replacePosition(pos1=pos)

                elif not init2 and magnitude2 and 2 not in returndict:
                    returndict[2] = (pos, (pos[0] + ori2[0], pos[1] + ori2[1]))
                    mag2 = magnitude2
                    self.addPosition(pos2=pos)

                elif not init2 and magnitude2 and 2 in returndict and magnitude2 < mag2:
                    returndict[2] = (pos, (pos[0] + ori2[0], pos[1] + ori2[1]))
                    mag2 = magnitude2
                    self.replacePosition(pos2=pos)

            else:
                if not init1 and magnitude1 and 1 not in returndict:
                    returndict[1] = (pos, (pos[0] + orientation1[0], pos[1] + orientation1[1]))
                    mag1 = magnitude1

                elif not init1 and magnitude1 and 1 in returndict and magnitude1 < mag1:
                    returndict[1] = (pos, (pos[0] + orientation1[0], pos[1] + orientation1[1]))
                    mag1 = magnitude1

                elif not init2 and magnitude2 and 2 not in returndict:
                    returndict[2] = (pos, (pos[0] + orientation2[0], pos[1] + orientation2[1]))
                    mag2 = magnitude2

                elif not init2 and magnitude2 and 2 in returndict and magnitude2 < mag2:
                    returndict[2] = (pos, (pos[0] + orientation2[0], pos[1] + orientation2[1]))
                    mag2 = magnitude2

        if 1 not in returndict:
            returndict[1] = (None, None)
        if 2 not in returndict:
            returndict[2] = (None, None)

        return returndict