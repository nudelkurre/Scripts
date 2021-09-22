#!/usr/bin/env python

import os, sys

directory = sys.argv[1] + "/"

for root, dirs, files in os.walk(directory, topdown=True):
	pass
videofiles=list()
subtitles=list()

series = root.split("/")[0].split("(")[0]
season = root.split("/")[1].split("_")[1]

for i in files:
	extension = i.split(".")[-1]
	if(extension == "mp4" or extension == "txt"):
		videofiles.append(i)
	elif(extension == "srt" or extension == "vtt"):
		subtitles.append(i)
videofiles.sort()
subtitles.sort()
temp2 = 1 # To start temp2 at 1
for i in videofiles:
	extension = i.split(".")[-1]
	episode = str()
	if(len(str(temp2)) == 1):
		episode = "0" + str(temp2)
	else:
		episode = str(temp2)
	src = directory +  i
	dst = directory + series + "_S" + season + "E" + episode + "." + extension
#	print(dst)
	os.replace(src, dst)
	temp2 = temp2 + 1

temp2 = 1 # To start temp2 at 1
for i in subtitles:
	extension = i.split(".")[-1]
	episode = str()
	if(len(str(temp2)) == 1):
		episode = "0" + str(temp2)
	else:
		episode = str(temp2)
	src = directory +  i
	dst = directory + series + "_S" + season + "E" + episode + ".swe.default." + extension
#	print(dst)
	os.replace(src, dst)
	temp2 = temp2 + 1