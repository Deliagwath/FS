from SimpleCV import *

# Class for recording of video feed
# There were problems with SimpleCV's videostream
# Hence, it has been implemented using cv2 instead


class SaveVideo:

    vidname = None
    dataname = None
    fps = 10
    fill = False
    videostream = None
    frame_number = 1
    data_buffer = []

    def __init__(self, vidname):
        # print vidname

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

    def init_video_stream(self, frame_size):

        # SimpleCV's VideoStream was too unreliable in creating
        # working video files, hence OpenCV's recording function
        # is called and used instead.
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        self.videostream = cv2.VideoWriter(self.vidname, fourcc,
                                           10, frame_size, True)

    def get_name(self):
        return self.vidname

    def record(self, frame, data):

        # Write from buffer every 1 second
        # Since 10 fps on VideoStream
        if data is not None and self.frame_number % 100 == 0:
            self.write_data(False)
        elif data is not None:
            self.buffer_data(data)

        if self.videostream is None:
            self.init_video_stream(frame.size())
        self.videostream.write(frame.getNumpyCv2())
        self.frame_number += 1

    def buffer_data(self, data):
        self.data_buffer.append({self.frame_number: data})

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
