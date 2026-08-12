---
title: "为树莓派安装Chromeium"
date: 2016-09-21 06:47:22
tags:
  - 树莓派
  - Linux
  - 教程
categories:
  - 技术
---

### 缘由

基于 Debian 的 Linux 发行版大家应该都不陌生，树莓派自带的系统就是其中之一。问题是它自带的浏览器体验实在跟不上主流网页的需求，卡顿、兼容性差是常态，所以还是得把它换成 Chromium。
<!-- more -->

### 方法

只需要把下面代码复制到 Terminal 里运行就可以了：

```sh

wget https://dl.dropboxusercontent.com/u/87113035/chromium-browser-l10n_45.0.2454.85-0ubuntu0.15.04.1.1181_all.deb

wget https://dl.dropboxusercontent.com/u/87113035/chromium-browser_45.0.2454.85-0ubuntu0.15.04.1.1181_armhf.deb

wget https://dl.dropboxusercontent.com/u/87113035/chromium-codecs-ffmpeg-extra_45.0.2454.85-0ubuntu0.15.04.1.1181_armhf.deb

sudo dpkg -i chromium-codecs-ffmpeg-extra_45.0.2454.85-0ubuntu0.15.04.1.1181_armhf.deb

sudo dpkg -i chromium-browser-l10n_45.0.2454.85-0ubuntu0.15.04.1.1181_all.deb chromium-browser_45.0.2454.85-0ubuntu0.15.04.1.1181_armhf.deb
```

之后在启动菜单里面的 Internet 分类里选择 Chromium 就好了。

### 笔记

关于版本号，这个是算一个比较旧的版本，如果链接失效了或者无法下载，还请各位告知一下我。
