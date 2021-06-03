#!/usr/bin/env python
from __future__ import unicode_literals
import youtube_dl

templist_file = open('/home/emil/Nextcloud/Notes/Music to download.txt', 'r').read().split("\n")[1:]

while("" in templist_file):
    templist_file.remove("")

list_file = []
for i in templist_file:
    temp = i
    temp = temp.split("]")[1]
    temp = temp[1:-1]
    list_file.append(temp)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'vorbis'},
        {'key': 'FFmpegMetadata'
    }],
    'outtmpl': '%(album)s-%(title)s-%(id)s.%(ext)s'
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(list_file)