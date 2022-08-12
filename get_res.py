#!/usr/bin/env python3

import cv2
import os
import sys

#directory = "/home/emil/Videos/Series/Other/Heroes(2006)/"
directory = sys.argv[1]
#print(directory)

file_list = []
for root, dirs, files in os.walk(directory, topdown=True):
    for file in files:
        if("mp4" in file):
            file_list.append(f"{root}/{file}")

file_list.sort()

low_res = []
for name in file_list:
        vid = cv2.VideoCapture(name)
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        #print(f"{name}: {width}x{height}")
        if(width < 1280 and height < 720):
            low_res.append(f"{name}: {width}x{height}")


if(len(low_res) > 0):
    print(f"---------\nFiles with low res:\n")
    for i in low_res:
        print(i)