#!/usr/bin/env python3

from yt_dlp import YoutubeDL
import argparse
import json
import xml.etree.ElementTree as x
import os
from mutagen.oggvorbis import OggVorbis
import xml.dom.minidom

parser = argparse.ArgumentParser(description="Download videos from youtube to either mkv-videos or ogg-audio")
parser.add_argument(dest='type', choices=["music", "video"], help='Choose either music or video')
parser.add_argument(dest='url', nargs='+', help='Enter url to download')
parser.add_argument("--path", default=os.getcwd(), help="Used to set path instead of using current directory")
parser.add_argument("--metadata", action="store_false", help="Get only metadata of video")
parser.add_argument("--season", default="1", help="Add optional season")
args = parser.parse_args()

path = args.path

video_opts = {
    'outtmpl': f'{path}/%(channel)s/%(title)s[%(id)s].%(ext)s',
    'writesubtitles': True,
    'subtitleslangs': 'all',
    'nooverwrites': True,
    'quiet':  True,
    'no_warnings': True,
    'simulate': False,
    'restrictfilenames': True,
    'writesubtitles': True,
    'writethumbnail': True,
    'postprocessors': [{
        'key': 'FFmpegVideoRemuxer',
        'preferedformat': 'mkv'},
        {'key': 'FFmpegMetadata'},
        {'key': 'FFmpegThumbnailsConvertor',
        'format': 'jpg'},
        {'key': 'EmbedThumbnail'
    }]
}

music_opts = {
    'outtmpl': f'{path}/%(artist)s/%(album)s/%(title)s.%(ext)s',
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'restrictfilenames': False,
    'quiet':  True,
    'simulate': False,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'vorbis'},
        {'key': 'FFmpegThumbnailsConvertor',
        'format': 'jpg'},
        {'key': 'EmbedThumbnail',
    }],
}

def jsonnfo(fileinfo, filename):
    j_title = fileinfo["title"]
    j_plot = fileinfo["description"].lstrip("\n")
    j_director = fileinfo["uploader"]
    j_releasedate = fileinfo["upload_date"][:4] + "-" + fileinfo["upload_date"][4:6] + "-" + fileinfo["upload_date"][6:8]
    j_year = fileinfo["upload_date"][:4]
    j_genres = fileinfo["categories"]
    j_tags = fileinfo["tags"]
    j_uniqueid = fileinfo["id"]
    movie = x.Element("movie")
    episode = x.Element("episodedetails")
    
    title = x.SubElement(episode, "title")
    title.text = j_title
    showtitle = x.SubElement(episode, "showtitle")
    showtitle.text = j_director
    season = x.SubElement(episode, "season")
    season.text = args.season
    plot = x.SubElement(episode, "plot")
    plot.text = j_plot
    for g in j_genres:
        genre = x.SubElement(episode, "genre")
        genre.text = g
    for t in j_tags:
        tag = x.SubElement(episode, "tag")
        tag.text = t
    dateadded = x.SubElement(episode, "dateadded")
    dateadded.text = j_releasedate
    releasedate = x.SubElement(episode, "releasedate")
    releasedate.text = j_releasedate
    premiered = x.SubElement(episode, "premiered")
    premiered.text = j_releasedate
    aired = x.SubElement(episode, "aired")
    aired.text = j_releasedate
    watched = x.SubElement(episode, "watched")
    watched.text = "false"
    year = x.SubElement(episode, "year")
    year.text = j_year
    uniqueid = x.SubElement(episode, "uniqueid")
    uniqueid.text = j_uniqueid
    uniqueid.set("type", "Youtube")
    locked = x.SubElement(episode, "lockdata")
    locked.text = "true"
    output = x.ElementTree(episode)
    output.write("tempfile")
    dom = xml.dom.minidom.parse("tempfile")
    xml_content = dom.toprettyxml()
    os.remove("tempfile")
    output_filename = f"{filename.split('.')[0]}.nfo"
    print(output_filename)
    f = open(output_filename, "w")
    f.write(xml_content)
    f.close()

def musicMetadata(fileinfo, filename):
    ogg = OggVorbis(filename)
    ogg['TITLE'] = fileinfo['title']
    ogg['ARTIST'] = fileinfo['artist']
    ogg['ALBUM'] = fileinfo['album']
    ogg['DATE'] = str(fileinfo['release_year'])
    ogg['TRACKNUMBER'] = fileinfo['playlist_index'] if fileinfo['playlist_index'] else '0'
    print(ogg.pprint())
    ogg.save()

urls = args.url

if(args.type == "music"):
    for url in urls:
        with YoutubeDL(music_opts) as ydl:
            info = ydl.extract_info(url, download=args.metadata)
            info_json = ydl.sanitize_info(info)
            filename = ydl.prepare_filename(info_json).split(".")[0] + ".ogg"
            musicMetadata(info_json, filename)
elif(args.type == "video"):
    for url in urls:
        with YoutubeDL(video_opts) as ydl:
            info = ydl.extract_info(url, download=args.metadata)
            info_json = ydl.sanitize_info(info)
            filename = ydl.prepare_filename(info_json).split(".")[0]
            try:
                jsonnfo(info_json, filename)
            except FileNotFoundError:
                print("Need to download video before creating metadata nfo")
else:
    print("Type need to be either video or music")