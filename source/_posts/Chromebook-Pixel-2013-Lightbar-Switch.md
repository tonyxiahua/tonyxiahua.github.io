---
title: "Chromebook Pixel 2013 Lightbar Switch"
date: 2017-01-06 09:54:13
tags:
  - Pixel
  - ChromenOS
categories:
  - 技术
---

Chromebook Pixel 2013 顶盖上有一条灯带（lightbar），开机、充电、干活的时候都会一闪一闪，设计感是有了，但晚上在暗处用电脑的时候真的挺刺眼。找了一下发现这条灯带其实是可以手动开关的，记录一下方法。
<!-- more -->

进入开发者模式之后，在 crosh（`Ctrl+Alt+T` 打开 Crosh，输入 `shell` 进入 Linux shell）里可以直接用 `ectool` 控制灯带：

```
sudo ectool lightbar off   # 关闭灯带
sudo ectool lightbar on    # 恢复默认显示
```

如果只是想在开会、看电影这种场合临时关一下，用这条命令比每次都进系统设置里翻半天方便多了。缺点是重启之后会恢复默认状态，想要开机自动关闭的话，得把这条命令写进启动脚本里。
