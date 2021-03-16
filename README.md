# gazetracker-with-heatmap
 An application to detect and map attention points on screen.

## Installing the required modules for running the project

To install the requirements from `requirements.txt` please run:

`pip install -r requirements.txt`

Alternatively the requirements could also be installed by running seperate `pip` commands for each entry in the `requirements.txt` file. This can be done as shown below.

`pip install numpy`

`pip install opencv-python`

`pip install autopy`

`pip install matplotlib`

`pip install seaborn`

`pip install Pillow`

`pip install pyscreenshot`

`pip install PyAutoGUI`


## Instructions for running the scripts

The project primarily contains two  scripts `image-gazetracker.py` that contains the code for gaze tracking on single static images and `video-gazetracker.py` that contains the code for generating gaze tracking points for dynamic elements such as when a person is scrolling a website or watching a video.

## To run image gaze tracking script

To run the image gaze tracking script run `cd` to the project folder from the terminal, fire up a terminal and run the following command.

`python image-gazetracker.py`

After the script fires up, it open's up the `open-cv` window where you can see you eyes getting tracked. Minimize this window. 

Next open up the content and after you're done open up the `open-cv` window again and press the `Esc` (escape key) to generate the scatter plot and the heatmap.

The scatter-plot pops up on the screen. Press Esc again to view the heatmap. These maps would also be save in the parent directory with the names `Output_Scatter.png` and `Output_heatmap.png`.

A demo of the output produced is shown below.

Gaze Scatter Plot
![Output_Scatter](https://github.com/null-buster/gazetracker-with-heatmap/blob/master/Output_Scatter.png)

Gaze Heatmap Plot
![Output_heatmap](https://github.com/null-buster/gazetracker-with-heatmap/blob/master/Output_heatmap.png)

Note: You must not close your content after pressing the escape key as the script takes a screenshot of the content on the screen after you close the open-cv window. 

## To run the video gaze tracking script(or to generate gaze tracking points on any dynamic data)

To run the video gaze tracking script run `cd` to the project folder from the terminal, fire up a terminal and run the following command.

`python video-gazetracker.py`


After the script fires up, it open's up the `open-cv` window where you can see you eyes getting tracked. Minimize this window. 

Next open up the content and after you're done open up the `open-cv` window again and press the `Esc` (escape key). This would generate the video containing the scatter plot data superimposed on each of the frames. 

Note: The script sampled at 30FPS on my laptop to generate the output so I had to slow down the video from an external source to get the slowed output.

![Scrolling Demo](https://github.com/null-buster/gazetracker-with-heatmap/blob/master/New%20Scrolling%20Demo.gif)
