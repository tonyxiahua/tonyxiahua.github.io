---
title: "ShadowSocks on Chromebook"
date: 2017-01-13 20:10:57
tags:
  - Chromebook
  - ShadowSocks
categories:
  - 技术
---

本文转载自 <http://www.zhyi828.com/shadowsocks-on-chromebook.html#comment-259>，介绍如何在 Chromebook 上用 ShadowSocks 科学上网。前提是你已经有自己的 SS 账号，账号怎么来的这里不展开。在 CB 上用 SS 科学上网主要有以下两种方法。
<!-- more -->

## 一、在 crouton 或 Dev OS 中开启 SS

这种方法需要在 CB 上通过 crouton 装好 Linux，或者直接装好 Dev OS，并且已经在里面成功连接了 SS。

1. 回到 ChromeOS，在 Chrome 商店里找到 Proxy SwitchyOmega 并添加至 Chrome。
2. 添加成功后，Chrome 右上角会出现 SwitchyOmega 标志，进入选项，点击左边栏新建情景模式，名称自选，选择"代理服务器"模式，选择 ss for cb 解压后的文件夹。
3. 代理协议选 SOCKS5，代理服务器填本地地址 127.0.0.1，端口与 SS 的本地代理端口相同，这里以 1080 为例。
4. 保存后再次新建，选择"自动切换"模式，规则列表选之前配置好的 SS，规则列表格式选 AutoProxy，规则列表网址填 `https://autoproxy-gfwlist.googlecode.com/svn/trunk/gfwlist.txt`，然后点"立即更新情景模式"，正文中出现地址列表即为成功。
5. 需要科学上网的时候，选择刚刚这个自动切换模式即可。

## 二、在原生 Chrome OS 中开启 SS

安装 shadowsocks for chromebook，源码在 [Github](https://github.com/shadowsocks/shadowsocks-chromeapp)，国内也有 zohead 编译好的版本可以直接用：[Baidu Pan](http://pan.baidu.com/s/1e1i4Q)，下载解压即可。

在扩展程序页面 `chrome://extensions/` 里勾上"开发者模式"，就能安装自己下载的第三方 app 了，点"加载正在开发的扩展程序"，选中刚刚解压的文件夹。填入服务器、端口、密码，保存后窗口不会自动关闭，把它最小化就行。之后再下载安装 SwitchyOmega，配置好切换规则，就能科学上网了。

至此两种方法已经介绍完毕，感谢 Unee Wang 和 Zohead 两位大神的帮助！

> 声明：本文仅供学术讨论之用，任何利用本文提到之方法做出的违反我国法律法规等行为，本人概不负责。
