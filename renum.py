#!/usr/bin/env python

import os, sys, re

directory = sys.argv[1] + "/"

for root, dirs, files in os.walk(directory, topdown=True):
	pass
videofiles=list()
subtitles=list()

series = root.split("/")[0].split("(")[0]
season = root.split("/")[1].split("_")[1]
episodename = re.compile("\_S\d+E\d+\.")

for i in files:
	extension = i.split(".")[-1]
	if(extension == "mp4" or extension == "txt"):
		videofiles.append(i)
	elif(extension == "srt" or extension == "vtt" or extension == "ass"):
		subtitles.append(i)
videofiles.sort()
subtitles.sort()
# temp2 = 1 # To start temp2 at 1
for i in videofiles:
	extension = i.split(".")[-1]
	episode = i.split(".")[0]
	# if(len(str(temp2)) == 1):
	# 	episode = "0" + str(temp2)
	# else:
	# 	episode = str(temp2)
	if(episodename.search(i)):
		continue
	src = directory +  i
	dst = directory + series + "_S" + season + "E" + episode + "." + extension
	# print(src, dst)
	os.replace(src, dst)
	# temp2 = temp2 + 1

# temp2 = 1 # To start temp2 at 1
for i in subtitles:
	extension = i.split(".")[-1]
	# episode = i.split(".")[0]
	# if(len(str(temp2)) == 1):
	# 	episode = "0" + str(temp2)
	# else:
	# 	episode = str(temp2)
	if(episodename.search(i)):
		continue
	src = directory +  i
	dst = directory + series + "_S" + season + "E" + episode + ".eng." + extension
	# print(dst)
	os.replace(src, dst)
	# temp2 = temp2 + 1