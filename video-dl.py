#!/usr/bin/env python3

from yt_dlp import YoutubeDL
import argparse
import json
import xml.etree.ElementTree as x
import os
from mutagen.oggvorbis import OggVorbis
import xml.dom.minidom

parser = argparse.ArgumentParser(description="Download videos from youtube to either mkv-videos or ogg-audio")
# parser.add_argument(dest='type', choices=["music", "video"], help='Choose either music or video')
parser.add_argument(dest='url', nargs='+', help='Enter url to download')
parser.add_argument("--music", action="store_true", help="Download music video as music file")
parser.add_argument("--audio-only", dest="audio", action="store_true", help="Download audio from a video")
parser.add_argument("--path", default=os.getcwd(), help="Used to set path instead of using current directory")
parser.add_argument("--metadata", action="store_false", help="Get only metadata of video")
parser.add_argument("--season", help="Add optional season")
args = parser.parse_args()

path = args.path

playlist_number = dict()

video_opts = {
    'outtmpl': f'{path}/%(channel)s/%(upload_date.0:4)s/%(title)s[%(id)s].%(ext)s',
    'writesubtitles': True,
    'subtitleslangs': [
        'en',
        'sv'
    ],
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
        {'key': 'ModifyChapters'},
        {'key': 'FFmpegMetadata'},
        {'key': 'FFmpegThumbnailsConvertor',
        'format': 'jpg'},
        {'key': 'EmbedThumbnail'
    }]
}

audio_only_opts = {
    'outtmpl': f'{path}/%(channel)s/%(title)s/%(title)s[%(id)s].%(ext)s',
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'restrictfilenames': True,
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

playlist_opts = {
    'quiet': True,
    'dump_single_json': True
}

def jsonnfo(fileinfo, filename):
    j_title = fileinfo["title"]
    j_plot = fileinfo["description"].lstrip("\n")
    j_director = fileinfo["uploader"]
    j_releasedate = fileinfo["upload_date"][:4] + "-" + fileinfo["upload_date"][4:6] + "-" + fileinfo["upload_date"][6:8]
    j_year = fileinfo["upload_date"][:4]
    j_episode = "".join(j_releasedate.split("-")[1:])
    j_season = j_year if not args.season and j_year else "01"
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
    season.text = j_season
    episode_nr = x.SubElement(episode, "episode")
    episode_nr.text = j_episode
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
    f = open(output_filename, "w")
    f.write(xml_content)
    f.close()

def audioMetadata(fileinfo, filename):
    ogg = OggVorbis(filename)
    ogg['TITLE'] = fileinfo['title']
    ogg['ARTIST'] = fileinfo['uploader']
    ogg['ALBUM'] = fileinfo['title']
    ogg['DATE'] = str(fileinfo["upload_date"][:4] + "-" + fileinfo["upload_date"][4:6] + "-" + fileinfo["upload_date"][6:8]) if fileinfo['upload_date'] != None else ""
    ogg['TRACKNUMBER'] = "1"
    ogg['COMMENT'] = fileinfo["description"]
    ogg.save()

def musicMetadata(fileinfo, filename):
    ogg = OggVorbis(filename)
    ogg['TITLE'] = fileinfo['title']
    ogg['ARTIST'] = fileinfo['artist']
    ogg['ALBUM'] = fileinfo['album']
    ogg['DATE'] = str(fileinfo["release_date"][:4] + "-" + fileinfo["release_date"][4:6] + "-" + fileinfo["release_date"][6:8]) if fileinfo['release_date'] != None else ""
    ogg['TRACKNUMBER'] = str(playlist_number[fileinfo['webpage_url']]) if playlist_number[fileinfo['webpage_url']] else '0'
    ogg.save()

def extractPlaylistUrls(urls):
    url_arr = []
    for url in urls:
        with YoutubeDL(playlist_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            info_json = ydl.sanitize_info(info)
            if("entries" in info_json.keys()):
                for i in info_json["entries"]:
                    playlist_number[i["webpage_url"]] = i["playlist_autonumber"]
                    url_arr.append(i["webpage_url"])
            else:
                playlist_number[info_json["webpage_url"]] = ""
                url_arr.append(info_json["webpage_url"])
    return url_arr

urls = extractPlaylistUrls(args.url)

if(args.music):
    for url in urls:
        try:
            with YoutubeDL(music_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                info_json = ydl.sanitize_info(info)
                # filename = "".join(ydl.prepare_filename(info_json).split(".")[0:-1]) + ".ogg"
                # musicMetadata(info_json, filename)
        except FileNotFoundError as e:
            print(f"Error with file {e}")
else:
    for url in urls:
        if(args.audio):
            with YoutubeDL(audio_only_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                info_json = ydl.sanitize_info(info)
                filename = "".join(ydl.prepare_filename(info_json).split(".")[0:-1]) + ".ogg"
                audioMetadata(info_json, filename)
                print(f"{filename} downloaded")
        else:
            with YoutubeDL(video_opts) as ydl:
                info = ydl.extract_info(url, download=args.metadata)
                info_json = ydl.sanitize_info(info)
                filename = "".join(ydl.prepare_filename(info_json).split(".")[0:-1])
                try:
                    jsonnfo(info_json, filename)
                except FileNotFoundError:
                    print("Need to download video before creating metadata nfo,", info_json["uploader"], info_json["id"])
# else:
#     print("Type need to be either video or music")