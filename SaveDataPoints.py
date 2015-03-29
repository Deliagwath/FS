from SimpleCV import *
import math

# Class for recording of video feed
# There were problems with SimpleCV's videostream
# Hence, it has been implemented using cv2 instead


class SaveDataPoints:

    vidname = None
    dataname = None
    fps = 10
    fill = False
    frame_number = 1
    data_buffer = []

    def __init__(self, vidname):

        parsed = vidname.split('.')

        # Checking for .avi extension from name
        if parsed[-1] != 'avi':
            extension = 'avi'
            vidname = vidname + '.' + extension

        parsed = vidname.split('.')

        # If file exists, rename and create new file
        if os.path.exists(vidname):

            # Rename until an acceptible filename is found
            index = 1
            name = '.'.join(parsed[:-1])

            # Keep increasing file number if no valid name is found
            while True:
                name += '_' + str(index)
                if os.path.exists(name + '.' + extension):
                    name = '_'.join(name.split('_')[:-1])
                    index += 1
                else:
                    self.vidname = name + '.' + extension
                    break
        else:
            self.vidname = vidname

        name = '.'.join(self.vidname.split('.')[:-1])
        self.dataname = name + '.txt'

        # If file exists, remove and create new file
        if os.path.exists(self.dataname):
            os.remove(self.dataname)

        # Creates file for writing
        opened_file = open(self.dataname, 'w')
        opened_file.close()

    def get_name(self):
        return self.vidname

    def save_data(self, inputdata, detecteddata):

        self.buffer_data(inputdata, detecteddata)
        self.write_data(False)

    # Parses data into comma separated variable format
    def buffer_data(self, inputdata, detecteddata):

        strdata = ""
        down1 = inputdata[0]
        up1 = inputdata[1]
        down2 = inputdata[2]
        up2 = inputdata[3]
        fly1pos = detecteddata[1][0]
        fly2pos = detecteddata[2][0]
        fly1dir = detecteddata[1][1]
        fly2dir = detecteddata[2][1]

        costest1 = -1
        costest2 = -1
        one = None
        two = None

        # Calculate Euclidean Distances
        if fly1pos is not None:
            dist11 = sqrt(((fly1pos[0] - down1[0]) ** 2) + ((fly1pos[1] - down1[1]) ** 2))
            dist21 = sqrt(((fly1pos[0] - down2[0]) ** 2) + ((fly1pos[1] - down2[1]) ** 2))

        if fly2pos is not None:
            dist12 = sqrt(((fly2pos[0] - down1[0]) ** 2) + ((fly2pos[1] - down1[1]) ** 2))
            dist22 = sqrt(((fly2pos[0] - down2[0]) ** 2) + ((fly2pos[1] - down2[1]) ** 2))

        if fly1pos is not None and fly2pos is not None:

            if dist11 < dist12:
                one = dist11
                two = dist22
                if fly1dir is not None:
                    user1 = self.vectorize(down1, up1)
                    data1 = self.vectorize(fly1pos, fly1dir)
                    costest1 = self.costest(user1, data1)

                if fly2dir is not None:
                    user2 = self.vectorize(down2, up2)
                    data2 = self.vectorize(fly2pos, fly2dir)
                    costest2 = self.costest(user2, data2)
            else:
                one = dist12
                two = dist21
                if fly1dir is not None:
                    user2 = self.vectorize(down2, up2)
                    data1 = self.vectorize(fly1pos, fly1dir)
                    costest1 = self.costest(user2, data1)

                if fly2dir is not None:
                    user1 = self.vectorize(down1, up1)
                    data2 = self.vectorize(fly2pos, fly2dir)
                    costest2 = self.costest(user1, data2)

        elif fly1pos is None and fly2pos is not None:
            if dist12 < dist22:
                one = dist12
                if fly2dir is not None:
                    user1 = self.vectorize(down1, up1)
                    data2 = self.vectorize(fly2pos, fly2dir)
                    costest1 = self.costest(user1, data2)
            else:
                one = dist22
                if fly2dir is not None:
                    user2 = self.vectorize(down2, up2)
                    data2 = self.vectorize(fly2pos, fly2dir)
                    costest1 = self.costest(user2, data2)

        elif fly1pos is not None and fly2pos is None:
            if dist11 < dist21:
                one = dist11
                if fly2dir is not None:
                    user1 = self.vectorize(down1, up1)
                    data1 = self.vectorize(fly1pos, fly1dir)
                    costest1 = self.costest(user1, data1)
            else:
                one = dist21
                if fly2dir is not None:
                    user2 = self.vectorize(down2, up2)
                    data1 = self.vectorize(fly1pos, fly1dir)
                    costest1 = self.costest(user2, data1)

            one = dist11 if dist11 < dist21 else dist21

        if one is not None:
            strdata = str(one)
        else:
            strdata = str(-1)

        strdata += "\n"

        if two is not None:
            strdata += str(two)
        else:
            strdata += str(-1)

        strdata += "\n"
        strdata += "," + str(costest1) + "\n"
        strdata += "," + str(costest2)

        self.data_buffer.append(strdata)

    def write_data(self, now):

        # print "write_data(" + str(now) + ")"
        # print "Buffer = " + str(self.data_buffer)

        # Writes to file
        opened_file = open(self.dataname, 'a')

        for data in self.data_buffer:
            opened_file.write(str(data) + "\n")

        self.data_buffer = []

        if now:
            opened_file.flush()

        # Close file
        opened_file.close()

    def end(self):
        self.write_data(True)

    def magnitude(self, vector):
        return math.sqrt(self.dot(vector, vector))

    def dot(self, vec1, vec2):
        return sum(p * q for p, q in zip(vec1, vec2))

    def vectorize(self, origin, end):
        return [a - b for a, b in zip(end, origin)]

    def costest(self, vec1, vec2):
        return self.dot(vec1, vec2) / (self.magnitude(vec1) * self.magnitude(vec2))