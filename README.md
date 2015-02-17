# FS
Honours Project Vision Processing

This readme is to explain the usage of the program.

First, the prerequisite to running the program is to install Python 2.7.3

https://www.python.org/download/releases/2.7.3/

And SimpleCV

http://simplecv.org/download

Then download the entire repository from github

https://github.com/Deliagwath/FS

to the directory you wish to run it from.

The program is very straight forward in running.
Open up the command prompt to the current working directory, and type in

python InitGUI.py

And the program should launch.

There are input parameters to take note of:
Camera Number:  Should default to 0, unless there are more than one cameras on the system,
                in which the number should be incremented by one each time to test out which
                camera to use.
                For Example, a laptop has an inbuilt webcam (Number 0) and we want to use the
                high definition USB camera just recently plugged in (Assigned Number 1 by system)
                we would then put 1 into the box to the right of the Camera Number label.

File Name:      This is a little less intuitive. If there is a pre-existing video file that needs
                to be analysed, it is to be inputted there in a folder called Test_Data in the same
                directory. In this case, Camera Number should be set to 0.
                If a live feed is needed, delete everything from said box, and it will initiate a
                live feed from specified camera.

Tracking:       Name should be self explanitory, it is a choice whether or not the system should
                track the flies and draw annotations onto the video feed.

Saving/Loading: This is a filename in which the circle you specify into the program is either saved
                to or loaded from depending on the tickbox underneath.
                For example, we have a set of lab equipment in which the arena will never be moved.
                In this case, we would only need to specify the area once and we can save it in a file
                and the next time the program runs, and the same filename is specified with the load
                box ticked, the program will initialise with the area already selected to minimise
                user input into the program.

File to record: This is the filename in which the program will attempt to record to when specified in
                the main loop of the program to record to.
                If the filename already exists, it will append a number behind the file in increments
                of one to not overwrite any existing data.
                If tracking is enabled, the orientation information will also be exported in a file
                of the same name, but with a .txt extension.
