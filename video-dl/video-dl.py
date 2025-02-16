#!/usr/bin/env python3

from yt_dlp import YoutubeDL
import yt_dlp
import argparse
import sys
import json
import xml.etree.ElementTree as x
import os
from mutagen.oggvorbis import OggVorbis
import xml.dom.minidom
import time
import re
from datetime import date

today = date.today().strftime("%Y-%m-%d")

parser = argparse.ArgumentParser(description="Download videos from youtube to either mkv-videos or ogg-audio")
parser.add_argument(dest='url', nargs='+', help='Enter url to download')
parser.add_argument("--music", action="store_true", help="Download music video as music file")
parser.add_argument("--audio-only", dest="audio", action="store_true", help="Download audio from a video")
parser.add_argument("--path", default=os.getcwd(), help="Used to set path instead of using current directory")
parser.add_argument("--metadata", action="store_false", help="Get only metadata of video")
parser.add_argument("--locked", action="store_true", help="Set the locked tag inside nfo metadata (only used for videos)")
parser.add_argument("--season", help="Add optional season")
args = parser.parse_args()

path = args.path

playlist_number = dict()

subtitleslangs = ['en', 'sv']

video_opts = {
    'outtmpl': f'{path}/%(id)s.%(ext)s',
    'writesubtitles': True,
    'subtitleslangs': subtitleslangs,
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
    'outtmpl': f'{path}/%(id)s.%(ext)s',
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
    'outtmpl': f'{path}/%(id)s.%(ext)s',
    'format': 'bestaudio/best',
    'writethumbnail': True,
    'restrictfilenames': False,
    'quiet':  True,
    'noprogress': False,
    'no_warnings': True,
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
    'dump_single_json': True,
    'noprogress': True,
    'no_warnings': True
}

def jsonnfo(fileinfo, filename):
    j_title = fileinfo["title"]
    j_plot = fileinfo["description"].lstrip("\n") if "description" in fileinfo.keys() else ""
    j_director = fileinfo["uploader"] if "uploader" in fileinfo.keys() else "NoName"
    j_releasedate = fileinfo["upload_date"][:4] + "-" + fileinfo["upload_date"][4:6] + "-" + fileinfo["upload_date"][6:8] if "upload_date" in fileinfo.keys() else today
    j_year = fileinfo["upload_date"][:4] if "upload_date" in fileinfo.keys() else today[:4]
    j_episode = "".join(j_releasedate.split("-")[1:])
    j_season = j_year if not args.season and j_year else "01"
    j_genres = fileinfo["categories"] if "categories" in fileinfo.keys() else ""
    j_tags = fileinfo["tags"] if "tags" in fileinfo.keys() else ""
    j_uniqueid = fileinfo["id"] if "id" in fileinfo.keys() else ""
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
    locked.text = str(args.locked).lower()
    output = x.ElementTree(episode)
    output.write("tempfile")
    dom = xml.dom.minidom.parse("tempfile")
    xml_content = dom.toprettyxml()
    os.remove("tempfile")
    output_filename = f"{filename}.nfo"
    f = open(output_filename, "w")
    f.write(xml_content)
    f.close()

def audioMetadata(fileinfo, filename):
    ogg = OggVorbis(filename)
    ogg['TITLE'] = fileinfo['title']
    ogg['ARTIST'] = fileinfo['uploader']
    ogg['ALBUM'] = fileinfo['title']
    ogg['DATE'] = str(fileinfo["upload_date"][:4] + "-" + fileinfo["upload_date"][4:6] + "-" + fileinfo["upload_date"][6:8]) if fileinfo['upload_date'] != None else ""
    ogg['ORIGINALYEAR'] = str(fileinfo["upload_date"][:4]) if fileinfo['upload_date'] != None else ""
    ogg['TRACKNUMBER'] = "1"
    ogg['COMMENT'] = fileinfo["description"]
    ogg.save()

def musicMetadata(fileinfo, filename):
    ogg = OggVorbis(filename)
    ogg['TITLE'] = fileinfo['title']
    ogg['ARTIST'] = fileinfo['artists'][0]
    ogg['ALBUM'] = fileinfo['album']
    ogg['DATE'] = str(fileinfo["release_date"][:4] + "-" + fileinfo["release_date"][4:6] + "-" + fileinfo["release_date"][6:8]) if fileinfo['release_date'] != None else str(fileinfo["upload_date"][:4] + "-" + fileinfo["upload_date"][4:6] + "-" + fileinfo["upload_date"][6:8]) if fileinfo['upload_date'] != None else ""
    ogg['ORIGINALYEAR'] = str(fileinfo["release_date"][:4]) if fileinfo["release_date"] != None else str(fileinfo["upload_date"][:4]) if fileinfo["upload_date"] != None else ""
    ogg['TRACKNUMBER'] = str(playlist_number[fileinfo['id']]) if str(playlist_number[fileinfo['id']]) else '0'
    ogg.save()

def extractPlaylistUrls(urls):
    url_arr = []
    for u in range(len(urls)):
        print(f"Get playlist {u + 1} of {len(urls)}")
        with YoutubeDL(playlist_opts) as ydl:
            info = ydl.extract_info(urls[u], download=False)
            info_json = ydl.sanitize_info(info)
            if("entries" in info_json.keys()):
                for i in info_json["entries"]:
                    playlist_number[i["id"]] = i["playlist_index"] if i["playlist_index"] else i["playlist_autonumber"]
                    url_arr.append(i["webpage_url"])
            else:
                playlist_number[info_json["id"]] = ""
                url_arr.append(info_json["webpage_url"])
        time.sleep(1)
        print("\033[A\033[J", end='\r')
    print("Playlists extracted")
    return url_arr

def renameFiles(filename, dest, dest_filename, exts):
    if not os.path.exists(dest):
        os.makedirs(dest)
    for ext in exts:
        os.rename(f"{filename}.{ext}", f"{dest}/{dest_filename}.{ext}")

    for lang in subtitleslangs:
        if os.path.exists(f"{filename}.{lang}.vtt"):
            os.rename(f"{filename}.{lang}.vtt", f"{dest}/{dest_filename}.{lang}.vtt")

def cleanName(name):
    return re.sub(r'[\W]+', "_", name)

def downloadMusic(url):
    with YoutubeDL(music_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        info_json = ydl.sanitize_info(info)
        filename = f"{info_json['id']}"
        musicMetadata(info_json, f"{filename}.ogg")
        album_name = re.sub(r'\-+|\/+', "-", info_json['album'])
        title = re.sub(r'\-+|\/+', "-", info_json['title'])
        dest = f"{path}/{info_json['artists'][0]}/{album_name}/"
        if(playlist_number[info_json['id']]):
            filenum = playlist_number[info_json['id']] if len(str(playlist_number[info_json['id']])) >= 2 else f"0{playlist_number[info_json['id']]}"
            destfile = f"{filenum} {title}"
        else:
            destfile = f"{title}"
        exts = ["ogg"]
        renameFiles(filename, dest, destfile, exts)

def downloadAudio(url):
    with YoutubeDL(audio_only_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        info_json = ydl.sanitize_info(info)
        filename = f"{info_json['id']}"
        audioMetadata(info_json, f"{filename}.ogg")
        dest = f"{path}/{cleanName(info_json['channel'])}/{cleanName(info_json['title'])}/"
        renameFiles(filename, dest, cleanName(info_json['title']), ["ogg"])

def downloadVideo(url):
    with YoutubeDL(video_opts) as ydl:
        info = ydl.extract_info(url, download=args.metadata)
        info_json = ydl.sanitize_info(info)
        filename = f"{info_json['id']}"
        jsonnfo(info_json, filename)
        dest = f"{path}/{cleanName(info_json['channel'])}/{info_json['upload_date'][0:4]}/" if "channel" in info_json.keys() and "upload_date" in info_json.keys() else f"{path}/NoName/{today[0:4]}/"
        if(not args.metadata):
            exts = ["nfo"]
        else:
            exts = ["mkv", "nfo"]
        renameFiles(filename, dest, f"{cleanName(info_json['title'])}[{info_json['id']}]", exts)

try:
    if(args.locked and (args.music or args.audio)):
        print("Locked only used for videos")
        exit(1)
    urls = extractPlaylistUrls(args.url)

    for u in range(len(urls)):
        retries = 3
        errors = []
        for r in range(retries):
            print(f"Download file {u + 1} of {len(urls)}, try {r + 1} of {retries}")
            try:
                if(args.audio):
                    downloadAudio(urls[u])
                elif(args.music or sys.argv[0].split("/")[-1] == "music-dl"):
                    downloadMusic(urls[u])
                else:
                    downloadVideo(urls[u])
            except FileNotFoundError as e:
                errors.append(str(e))
            except yt_dlp.utils.DownloadError as e:
                errors.append(str(e))
                time.sleep(2)
                print("\033[A\033[J]", end='\r')
            else:
                break
            finally:
                print("\033[A\033[J]", end='\r')
        else:
            with open("video-dl-errors.log", "a") as f:
                errorsText = f"URL: {urls[u]}\nError: {''.join(errors)}"
                f.write(errorsText)
    print("All files downloaded", end='\n')
except KeyboardInterrupt:
    print("\nExiting")
