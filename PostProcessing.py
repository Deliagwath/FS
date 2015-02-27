import os


class PostProcessing:

    datanames = []

    def __init__(self, vidname):
        parsed = vidname.split('.')

        # Changing .avi to .txt for data storage
        self.dataname = '.'.join(parsed[:-1]) + '.txt'

    def post_process(self):
        if not os.path.exists("PostProcessing"):
            return False
        else:
            with open("PostProcessing", 'r') as input_file:
                self.datanames = input_file.readlines()
                input_file.close()

        for videodata in self.datanames:

            os.rename(videodata, "temp.txt")

            read_file = open("temp.txt", 'r')
            write_file = open(videodata, 'w')

            for line in read_file:

                try:
                    parsed = eval(line)

                    for frame, data in parsed.iteritems():
                        write_file.write(str(frame))

                        for fly, flydata in data.iteritems():
                            origin, destination = flydata
                            if origin is None:
                                write_file.write(',' + str(None))
                            else:
                                x1, y1 = origin
                                write_file.write(',' + str(x1))
                                write_file.write(',' + str(y1))

                            if destination is None:
                                write_file.write(',' + str(None))
                            else:
                                x2, y2 = destination
                                write_file.write(',' + str(x2))
                                write_file.write(',' + str(y2))

                        write_file.write('\n')

                except SyntaxError:
                    write_file.write(line)

            read_file.close()
            write_file.close()
            os.remove("temp.txt")
        os.remove("PostProcessing")