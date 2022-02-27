# screen-timelapse
A simple python script that takes a screenshot every X seconds and then converts those screenshots into a timelapse.

## Getting started 
Install the required packages by running 

`pip install -r requirements.txt`

Then simply start the script by running

`python3 screen_timelapse.py`

This will begin taking screenshots every X seconds. Hit Crlt+C when you wish to end capturing screenshots and you'll
be presented with the option to convert screenshots from your session to a timelapse. 

## Arguments: 
```
  -h, --help            show this help message and exit
  -c, --convert         convert screenshots to a timelapse
  -d SECONDS, --delay SECONDS
                        modify the delay between screenshots. default is 10
  --fps FPS             modify the frames per second of the timelapse. default is 2
```