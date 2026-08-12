---
title: "BiliBili live Danmu on Mac (OS X)"
date: 2016-06-09 15:23:56
tags:
  - Bilibili
  - 直播
  - 弹幕
  - 科技
categories:
  - 技术
---

## Start up

BiliBili live streaming has been booming lately, and plenty of people are getting into broadcast tools like OBS and CopyLiu's Danmu client for Windows. The catch: those tools only really target Windows. Users on a Macbook or Linux box are stuck with an unfriendly, mostly Windows-first software ecosystem — so we don't get the same Danmu experience out of the box.

I'm one of those Mac users, and after a few days of digging I found a workaround. [Octavian's project](https://github.com/OctavianLee/Barrage) uses Python to build a command-line tool that shows the user message feed and live channel count right in your Terminal — basically a lightweight Danmu client that works anywhere Python runs.
<!-- more -->

Here's the installation tutorial:

### Step 1

Open your Terminal, Use the command to enter your unzip folder:  
```bash
cd YOUR-FOLDER-LOCATION
```

### Step 2

Then You have installed the latest Python. [Go to the website download the Python for Mac.](https://www.python.org/downloads/mac-osx)

**Tips. I recommend download the Python 3.**

### Step 3

Use the pip command to build meet the requirement of the software.  
```bash
pip install -r requirements.txt
```

### Step 4

Run the python command line(NO GUI).  
```bash
python main.py
```

### Summary

If you successfully run those commands above, you should see a selection menu on the screen. Type "1" to pick a room number and start receiving messages from that channel, or type "2" to log into Bilibili and send messages from your own account — though that second option hasn't worked reliably for me, since BiliBili keeps changing their API.

Once you've got it running, your Danmu Machine will sit in the Terminal refreshing the live channel watcher count every 5 seconds while streaming in the message feed. Nice day.
