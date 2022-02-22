import os
import glob
import time
import signal
import argparse
from datetime import datetime

import cv2
import PIL.ImageGrab


def capture_start(capture_delay=10):
    print("delay is {}".format(capture_delay)) # debugging
    print("Press Ctrl+C to stop capturing...")

    if not os.path.exists("./screenshots"):
                os.mkdir("./screenshots")
    else: 
        # remove screenshots from previous session
        files = glob.glob("./screenshots/*")
        files = [f.replace("\\", "/") for f in files] # silly windows
        for file in files:
            os.remove(file)

    count = 0

    while True:
            PIL.ImageGrab.grab().save("screenshots/" + "screenshot {}.png".format(count))

            count += 1

            time.sleep(capture_delay)

def capture_end(*args):
    while True:
        convert_option = input("Would you like to convert screenshots to a timelapse now? [y/n]").lower().strip()

        if convert_option != "n" and convert_option != "y":
            print("Invalid option!")
            continue

        if convert_option == "y":
            convert()
        elif convert_option == "n":
            exit(0)
    

def convert(video_fps=2):
    print("video fps is {}".format(video_fps)) # debugging
    if not os.path.exists("./screenshots"):
        raise FileNotFoundError("Screenshots directory does not exist.")

    screenshots = sorted(
        glob.glob(os.path.abspath(os.getcwd()) + "/screenshots/screenshot *.png"), 
        key = lambda number: int(number[len(os.path.abspath(os.getcwd()) + "/screenshots/screenshot"):][:-4])
        )
        # probably could've used a regular expression in the above line but oh well

    screenshots = [ss.replace("\\", "/") for ss in screenshots] # silly windows

    height, width, _ = cv2.imread(screenshots[0]).shape
   
    filename = datetime.today().strftime("%d-%m-%Y") + ".mp4" # set filename to current date

    if os.path.exists(filename): # if filename exists, give option to create a new file or override exisiting
        while True:
            print("Timelapse with the same filename already exists.")
            n = input("Type 1 to override or type 2 to create a new file...").strip()
            if n != "1" and n != "2":
                print("Invalid option!")
                continue 

            if n == "1":
                break

            elif n == "2":
                filename = filename[:-4] + "-copy" + ".mp4"
                break 

    print("Please wait while screenshots are being converted to video...")

    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*"mp4v"), video_fps, (width, height))

    for screenshot in screenshots:
        out.write(cv2.imread(screenshot))

    out.release()

    while True:
        delete= input("Screenshots have been converted to video. Would you like to delete screenshots? [y/n]").lower().strip()
        if delete != "n" and delete != "y":
            print("Invalid option!")
            continue

        if delete == "y":
            files = glob.glob('./screenshots/*')
            files = [f.replace("\\", "/") for f in files] # silly windows
            for file in files:
                os.remove(file)
            exit(0)
        elif delete == "n":
            exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="record a timelapse of your screen")
    parser.add_argument("-c", "--convert", help="convert screenshots to a timelapse" ,action="store_true")
    parser.add_argument("-d", "--delay", help="modify the delay between screenshots. default is 10", type=int, default=10)
    parser.add_argument("--fps", help="modify the frames per second of the timelapse. default is 2", type=int, default=2)

    args = parser.parse_args()

    if (args.convert):
        convert(args.fps)

    else:
        signal.signal(signal.SIGINT, capture_end)
        capture_start(args.delay)