#!/usr/bin/env python

import os, sys
from pathlib import Path
from tinytag import TinyTag

directory = sys.argv[1] + "/"

f = []
for root, dirs, files in os.walk(directory, topdown=True):
    f.extend(files)
    break
#temp=f
f.sort()
print(f)

#for i in files:
#    tempstr = i.split("-")
#    print(len(tempstr))
#    if(len(tempstr) == 3):
#        sep = "/"
#        templist = list()
#        templist.append(tempstr[0].lstrip().rstrip())
#        templist.append(tempstr[1].lstrip().rstrip())
#        templist.append(tempstr[2].lstrip().rstrip())
#        path = sep.join(templist)
        
        #temp.append(path)
        #print(i, path)

#        tempdir = directory + sep.join(path.split("/")[0:2])
#        Path(tempdir).mkdir(parents=True, exist_ok=True)
#        print(tempdir)

 #       src = directory + i
 #       dst = directory + path
 #       print(src, dst)
 #       os.replace(src, dst)
#        break

#print(temp)

for i in f:
    file_format = "." + i.split(".")[-1]
    tag = TinyTag.get(i)
    if(len(tag.track) < 2):
        padded_tracknr = "0" + tag.track
    else:
        padded_tracknr = tag.track
    trackname = padded_tracknr + " " + tag.title + file_format

    sep = "/"
    templist = list()
    templist.append(tag.artist.lstrip().rstrip())
    templist.append(tag.album.lstrip().rstrip())
    templist.append(trackname.lstrip().rstrip())
    path = sep.join(templist)
    print(path)

    tempdir = directory + tag.artist + "/" + tag.album + "/"
    Path(tempdir).mkdir(parents=True, exist_ok=True)
    print(tempdir)

    src = directory + i
    dst = directory + path
    print(src, dst)
    os.replace(src, dst)