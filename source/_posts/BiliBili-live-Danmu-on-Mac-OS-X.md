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

Recently, BiliBili is in a boost of the user watching live channel, also many people start their business of using how to get started using the live broadcast softwares. Such as the OBS, and CopyLiu’s Danmu for Windows operating system. As a matter of fact, some user has Macbook or some Linux computer, they are facing a severe condition of unfriendly Chinese Software developing environment. Windows is also in the highest priority than other systems, and user of Mac the face become :( So I am one of them, after a few days struggling, I found some replaceable ways to access the Danmu function like in Windows. Let’s have a look.

I found the project of [Octavian](https://github.com/OctavianLee/Barrage). He uses Python to make a command line tool which shows : User Message & Live Channel Count. (in Terminal).

Here is the installation tutorial:  
<!-- more -->

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

If you successfully run those commands above. You should see the selection menu on the screen.

Type “1” to select the room number, and receive the message from that channel.

Type “2” to login Bilibili, and find out the part to get access to your account and send messages. (But this function havn’t successed yet. BiliBili always changes their API)

If you've done those, you should have your Danmu Machine working in your Terminal. In every 5 seconds it shows the count of live channel watcher. Also receiving the message.

Nice day.
