from math import sqrt


class TrackingModule:

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
            self.init_weights()
            self.init_arrays()
        else:
            self.size = 1

    def init_arrays(self):

        for i in range(0, self.size):
            self.fly1past.append(None)
            self.fly2past.append(None)

        for i in range(0, self.size - 1):
            self.fly1pastori.append(None)
            self.fly2pastori.append(None)

    def init_weights(self):

        total = 0

        for i in range(1, self.size + 1):
            total += i

        self.weights = []
        for i in range(1, self.size + 1):
            self.weights.append(i / float(total))

    def within_range(self, flyno, pos):

        # Retrieving past data for calculation
        if flyno == 1:
            deltax = pos[0] - self.fly1past[-1][0]
            deltay = pos[1] - self.fly1past[-1][1]

        elif flyno == 2:
            deltax = pos[0] - self.fly2past[-1][0]
            deltay = pos[1] - self.fly2past[-1][1]

        else:
            print "Incorrect Arguments TrackingModule.py \
            withinRange(" + str(flyno) + ", " + str(pos) + ")"
            return False, None

        # Calculating magnitude of difference
        # between two points to attempt to retain identity
        magnitude = sqrt((deltax ** 2) + (deltay ** 2))

        if self.minrange < magnitude < self.maxrange:
            orientation = [(deltax / magnitude) * 1000,
                           (deltay / magnitude) * 1000]
            return magnitude, orientation
        else:
            return False, None

    def bulk_track(self, blobs):

        returndict = {}

        init1 = False
        init2 = False

        if blobs is None:
            return {1: (None, None), 2: (None, None)}

        for pos in blobs.coordinates():

            if self.fly1past[-1] is None:
                returndict[1] = (pos, None)
                init1 = True
                continue

            if self.fly2past[-1] is None:
                returndict[2] = (pos, None)
                init2 = True
                continue

            if init1 and init2:
                break

            # Checks if the new co-ordinates are within
            # range of the new co-ordinate
            if not init1:
                boolean1 = self.within_min(1, pos)

            if not init2:
                boolean2 = self.within_min(2, pos)

            if not init1 and boolean1:
                returndict[1] = (pos, boolean1)

            elif not init2 and boolean2:
                returndict[2] = (pos, boolean2)

        if 1 not in returndict:
            returndict[1] = (None, None)
        if 2 not in returndict:
            returndict[2] = (None, None)

        return returndict

    # Modification to withinRange which only checks
    # if the fly is stationary or not

    def within_min(self, flyno, pos):
        # Retrieving past data for calculation
        if flyno == 1:
            deltax = pos[0] - self.fly1past[-1][0]
            deltay = pos[1] - self.fly1past[-1][1]

        elif flyno == 2:
            deltax = pos[0] - self.fly2past[-1][0]
            deltay = pos[1] - self.fly2past[-1][1]

        else:
            print "Incorrect Arguments: TrackingModule.py \
                withinMin(" + str(flyno) + ", " + str(pos) + ")"
            return False, None

        # Calculating magnitude of difference between
        # two points to attempt to retain identity
        magnitude = sqrt((deltax ** 2) + (deltay ** 2))

        if 0 <= magnitude <= self.minrange:
            return True
        else:
            return False

    def set_range(self, minrange=None, maxrange=None):
        if minrange is None and maxrange is None:
            self.minrange = 1
            self.maxrange = 30
        if minrange is not None:
            self.minrange = minrange
        if maxrange is not None:
            self.maxrange = maxrange

    def add_position(self, pos1=None, pos2=None):

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

    def replace_position(self, pos1=None, pos2=None):

        if pos1 is not None:
            self.fly1past[-1] = pos1

        if pos2 is not None:
            self.fly2past[-1] = pos2

    def add_orientation(self, ori1=None, ori2=None):

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

    def replace_orientation(self, ori1=None, ori2=None):

        if ori1 is not None:
            self.fly1pastori[-1] = ori1

        if ori2 is not None:
            self.fly2pastori[-1] = ori2

    # Used for WMA (Weighted Moving Average) calculation
    # Takes previous orientations to calculate
    # an average of where the orientation should be
    def calculate_orientation(self):

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

    # Checks whether or not the program is tracking
    # both pointers to the same blob rather than two blobs
    # This case occurs when the two flies meet and forms one blob,
    # causing the program to move both trackers to that one blob.
    def check_incorrect_tracking(self):

        # Checks if x co-ords are the same and y co-ords are the same
        if self.fly1past[-1] is not None and self.fly2past[-1] is not None \
                and self.fly1past[-1][0] == self.fly2past[-1][0] \
                and self.fly1past[-1][1] == self.fly2past[-1][1]:
            return True
        else:
            return False

    # Returns a dictionary with the fly id as the key,
    # and two co-ordinates ((x,y), (x2,y2)) as values.
    def track(self, blobs):

        returndict = {}
        mag1 = 0
        mag2 = 0

        init1 = False
        init2 = False

        first = True

        orientation1 = None
        orientation2 = None

        # For the case in which both the trackers
        # are tracking the same object, reinitialise the class
        if self.check_incorrect_tracking():
            self.__init__(self.smoothingmethod, self.size)

        if blobs is None:
            return {1: (None, None), 2: (None, None)}

        for pos in blobs.coordinates():

            if self.fly1past[-1] is None:
                self.add_position(pos1=pos)
                returndict[1] = (pos, None)
                init1 = True
                continue

            if self.fly2past[-1] is None:
                self.add_position(pos2=pos)
                returndict[2] = (pos, None)
                init2 = True
                continue

            if init1 and init2:
                break

            # Checks if the new co-ordinates are
            # within range of the new co-ordinate
            if not init1:
                magnitude1, orientation1 = self.within_range(1, pos)

            if not init2:
                magnitude2, orientation2 = self.within_range(2, pos)

            # If smoothingmethod is Weighted Moving Average ("WMA")
            if self.smoothingmethod == "WMA":
                if first:
                    self.add_orientation(orientation1, orientation2)
                    first = False
                else:
                    self.replace_orientation(orientation1, orientation2)

                self.calculate_orientation()
                ori1, ori2 = self.calculate_orientation()

                if not init1 and magnitude1 and 1 not in returndict:
                    returndict[1] = (pos, (pos[0] + ori1[0], pos[1] + ori1[1]))
                    mag1 = magnitude1
                    self.add_position(pos1=pos)

                elif not init1 and magnitude1 and \
                        1 in returndict and magnitude1 < mag1:
                    returndict[1] = (pos, (pos[0] + ori1[0], pos[1] + ori1[1]))
                    mag1 = magnitude1
                    self.replace_position(pos1=pos)

                elif not init2 and magnitude2 and 2 not in returndict:
                    returndict[2] = (pos, (pos[0] + ori2[0], pos[1] + ori2[1]))
                    mag2 = magnitude2
                    self.add_position(pos2=pos)

                elif not init2 and magnitude2 and \
                        2 in returndict and magnitude2 < mag2:
                    returndict[2] = (pos, (pos[0] + ori2[0], pos[1] + ori2[1]))
                    mag2 = magnitude2
                    self.replace_position(pos2=pos)

            else:
                if not init1 and magnitude1 and 1 not in returndict:
                    returndict[1] = (pos, (pos[0] + orientation1[0],
                                           pos[1] + orientation1[1]))
                    mag1 = magnitude1

                elif not init1 and magnitude1 and \
                        1 in returndict and magnitude1 < mag1:
                    returndict[1] = (pos, (pos[0] + orientation1[0],
                                           pos[1] + orientation1[1]))
                    mag1 = magnitude1

                elif not init2 and magnitude2 and \
                        2 not in returndict:
                    returndict[2] = (pos, (pos[0] + orientation2[0],
                                           pos[1] + orientation2[1]))
                    mag2 = magnitude2

                elif not init2 and magnitude2 and \
                        2 in returndict and magnitude2 < mag2:
                    returndict[2] = (pos, (pos[0] + orientation2[0],
                                           pos[1] + orientation2[1]))
                    mag2 = magnitude2

        if 1 not in returndict:
            returndict[1] = (None, None)
        if 2 not in returndict:
            returndict[2] = (None, None)

        return returndict