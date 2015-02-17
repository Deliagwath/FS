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

Inside the program itself, you will be prompted with three or two screens depending whether or not you
loaded the file with the initialised area.

This will explain how it will work.

The first screen will be the area grab.

This will be the optional screen depending on if the file is loaded or not.
The aim of this screen is to reduce noise and reduce computation time by selecting the arena itself.
Left click and drag to create a circle in which will be used for computation. Release to lock it in place.
If the first circle is not satisfcatory, you can retry as many times as you want with the same method,
being left click and drag.
Once the area has been selected, either right click, or press ESC to proceed.

The second screen is the colour selector.

This screen will display three images.
The area you selected directly from the live feed with a mask to ignore the corners of the arena.
The purpose of this screen is to allow the user to choose the colour by clicking on the leftmost image
where they think will affect the other two images to the right the most.
The aim is to choose a colour in which will only display the two flies clearly.
The colour is initialised to [100, 100, 100] which is grey and is acceptible in the calculations.

The third screen is the main program loop.

This is where the main analysis and display overlay comes in.
The feed can be moved frame by frame by scrolling downwards using the mouse wheel, or left click to make
the feed continuous.
The feed can also be recorded as the leftmost image without annotation by right clicking until a red circle
appears at the bottom left hand corner.
Once done, you should right click again to turn the recording off, and you can proceed by pressing ESC
to end the program.
The left and right click may be required to be held down for the program to respond.

Then the GUI should still remain in place, allowing for more experimentation to be done.

In case the exact same or similar experiemnt is to be run, the save buttom will save the current
configurations in the GUI, to allow the user not to need to re-write all arguments to the program,
and will be automatically loaded the next time the program runs.
The program will then be stopped if the user presses the red X at the top right hand corner.
