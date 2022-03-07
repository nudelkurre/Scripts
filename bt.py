#!/usr/bin/env python

import subprocess
import json
import sys

id = sys.argv[1]
proc = subprocess.Popen(["upower","-d"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).communicate()[0].decode("UTF-8").split("\n\n")

device = ""
for i in proc:
	if(id.replace(":", "_") in i):
		device = i
device = device.split("\n")
bt_dict = {}
for i in device:
	splitted = i.split(":")
	if len(splitted) >= 2:
		key = splitted[0].lstrip().rstrip()
		value = ":".join(splitted[1:]).lstrip().rstrip()
		bt_dict[key] = value

if(bt_dict['native-path'] != "(null)"):
	print(f"{bt_dict['percentage']}")
else:
	print()