#!/usr/bin/env python

import subprocess

proc = subprocess.Popen(["headsetcontrol","-b", "-c"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
bat_level = proc.communicate()[0]
if(bat_level == b'0' or bat_level == b''):
	print("")
else:
	print(str(int(bat_level)) + "%")
