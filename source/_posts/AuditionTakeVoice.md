---
title: "Audition 消除伴奏获取人声的办法"
date: 2016-10-21 21:17:02
tags:
  - 后期处理
  - Audition
  - Adobe
categories:
  - 技术
---

很多时候网上根本找不到一首歌的伴奏或者清唱人声版本，与其到处找资源，不如用 Adobe Audition 自己动手把人声从完整的歌曲里分离出来——原理是利用左右声道的相位差，把居中的人声单独抠出来，虽然效果比不上专业分轨，但日常使用完全够了。
<!-- more -->

### 步骤

1. 使用Audition 打开你的歌曲
2. 在Effects里面找到 Stereo Imagery
3. 选择 Center Channel Extractor
4. 之后在里面的弹出的窗口第二个Tab里拉下选项，里面有你想要保留的项目，例如男声，女声，bass，还有noise。
5. 最后按Apply

### 尾语

其实是自己稍微记录一下Audition的一些常用功能。希望对大家有用。
