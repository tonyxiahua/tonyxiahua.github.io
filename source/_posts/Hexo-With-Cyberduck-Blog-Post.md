---
title: "Hexo With Cyberduck Blog Post"
date: 2016-11-22 23:02:47
categories:
  - 技术
---

这个网站是基于Linux的服务器，如何远程管理你的服务器是一节必修课。我的解决方案是使用Cyberduck + Putty（Windows平台）。 这两个工具几乎可以满足日常的博客维护需求。  
<!-- more -->

### Cyberduck 配置

Cyberduck 主要用来管理博客的静态文件，本质上就是一个带界面的SFTP客户端。

1. 打开Cyberduck，点击左上角"打开连接"
2. 协议选择SFTP（SSH File Transfer Protocol）
3. 填入服务器地址、端口（默认22）、用户名
4. 如果用密钥登录，在"SSH私钥"里选择你的private key文件
5. 连接成功之后就能像本地文件夹一样拖拽上传/下载hexo生成的public目录了

### Putty 配置

Putty 是用来远程登录服务器执行命令的，比如重启Nginx、看日志之类的操作。

1. Host Name填服务器IP
2. Port默认22，Connection type选SSH
3. 如果要用密钥登录，在Connection -> SSH -> Auth里加载你的.ppk私钥文件
4. 点Open就能连接，第一次连接会提示确认服务器指纹，选Yes就行

这两个工具一个管文件，一个管命令行，配合起来基本能覆盖日常的博客维护需求了。
