from math import sqrt

def withinRange(prevpos, pos, minrange, maxrange):
    deltax = pos[0] - prevpos[0]
    deltay = pos[1] - prevpos[1]
    magnitude = sqrt(deltax ** 2 + deltay ** 2)
    print "Magnitude:\t" + str(magnitude)
    if minrange < magnitude < maxrange:
        # print "prevpos:\t" + str(prevpos) + "\npos:\t" + str(pos)
        orientation = [(deltax / magnitude) * 10, (deltay / magnitude) * 10]
        return magnitude, orientation
    else:
        return False, None

# Returns a dictionary with the fly id as the key, and two co-ordinates ((x,y), (x2,y2)) as values.
def track(flyprevpos, blobs, minrange, maxrange):

    returndict = {}
    mag1 = 0
    mag2 = 0

    init = {1: False, 2: False}

    for index, pos in enumerate(blobs.coordinates()):

        if fly1prevpos is None:
            fly1prevpos = pos
            returndict[1] = (pos, None)
            init1 = True
            continue

        if fly2prevpos is None:
            fly2prevpos = pos
            returndict[2] = (pos, None)
            init2 = True
            continue

        if init1 and init2:
            break

        # Checks if the new co-ordinates are within range of the new co-ordinate
        if not init1:
            magnitude1, orientation1 = withinRange(fly1prevpos, pos, minrange, maxrange)

        if not init2:
            magnitude2, orientation2 = withinRange(fly2prevpos, pos, minrange, maxrange)

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