# RPI GUI
---
The purpose of this project is to maintain an informational display designed to be run on a raspberry pi.


## Assumptions

This project makes the following assumptions:

* You have a raspberry pi connected to a single display
* You have python3 installed with the PyQt5 and Pillow libraries, OR you have Docker intsalled

For certain information displays, you will need:

* A ClimaCell API Key (for outdoor weather info)
  * You can get one here: https://www.climacell.co/weather-api/

Entirely optional, but useful if you have it:

* Home Assistant

## Usage

#### With Docker (recommended)

Docker is the easiest way to use this project as it takes care of all the dependencies for you.

First, clone this repository, `cd rpi_gui`, then edit `secret.py` and `CONFIG.py` to your liking.

Then build the docker image (don't worry, the dockerfile is provided) by doing `docker image build .`

Once that is done, copy/paste the following docker command, replacing `IMAGE` with the string of letters and numbers you got from running the previous command:
```
docker run --rm \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /etc/localtime:/etc/localtime:ro \
  -e DISPLAY=:0 \
  -u qtuser \
  IMAGE \
  python3 /app/main.py
```

You may see some messages print afterwards; you can ignore these as long as the program is working. You will know it is working if an image appears on the display with the current time. You can close the command window (or terminate the ssh session) and the program will continue to run. 

To stop the program, you will have to find and terminate the processes manually. On Raspbian, this can be done by finding the process IDs using `ps -aux | grep python`. You will then have to kill 2 processes, the one for the Docker command and the one that says something like `python3 /app/main.py`.

#### Without Docker

Make sure PyQt5 is installed first. This could be tricky; `pip install pyqt5` did not work for me. Also install Pillow: `pip install pillow`.

Clone the repository, `cd rpi_gui`, and install the dependencies using the following command:

`git clone https://github.com/ClimaCell-API/weather-code-icons.git weather_icons/`

Make sure the variables in `secret.py` and `CONFIG.py` are set.
 
Then do `python main.py` to start the program.

To end the program, do Ctrl+C or terminate the ssh session. You can also press the Escape button if you have a keyboard connected to your Pi.

## Customization

You can add images to the `img` folder, and these images will be cycled through as the background. The images do not have a size requirement, but the width of the image should be greater than its height. Images that are closer to the dimensions of your display will work better.

There are also some minor customizations you can make by editing `main.py` by changing the values of the variables defined before the class. You can change:

* the length of time before the background photo changes
* font type and size of clock