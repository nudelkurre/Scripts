# Scripts

Small helper scripts

## Descriptions

All scripts except for video-dl prints the output in json format to be able to easily be used by other programs

#### bluetooth
Script used to report battery level of connected devices.

#### disk
Script that read all mounted disks and prints each mount points, name of disk for mount point, used space, used percentage and total size of disk.

#### network
Script that print all interfaces ip, subnet mask, broadcast address and connection status (connected/disconnected).

#### video-dl
Script that with help of yt-dlp is preconfigured to download videos as mkv files and audio/music as ogg and sort by channel name or artist. Audio and music gets metadata embedded into the files and videos gets metadata written to a nfo file to be used by media players with support for kodi/jellyfin format of nfo.

#### volume
Script that print current volume of default sink from pipewire or can change volume or mute sink or change default sink.

#### weather
Script that get weather data from SMHI api by enter the name of a Swedish city as parameter to the script when running it.

#### workspaces
Script that reports the names and ids of all workspaces per monitor and which workspace that is the current active one. Can also be used to either go to previous/next workspace or go to specified workspace.

## Installation
Each script that need more packages than python default have their own `requirements.txt` that can be used to install dependencies required by that script.
To install use `pip install -r requirements.txt` from a terminal inside the scripts directory.

### Nix
If nix is installed in the system, each script can be run by using `nix run github:nudelkurre/Scripts#<script name>` which then runs the script with all dependencies included.