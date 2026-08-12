---
title: "Chromebook Pixel 2013 Developer Mode"
date: 2016-12-04 09:49:04
tags:
  - Chromebook
  - Chrome
  - Pixel
categories:
  - 技术
---

## Why should I write this?

More and more people get stuck trying to gain superuser access to make changes on their computer.  
Those functions are disabled by the OEM by default — we need root access to unlock full functionality.
<!-- more -->

## How to enable Developer Mode

1. Power off the Chromebook.
2. Hold `Esc` + `Refresh`（F3）, then press the power button — this boots into the recovery screen.
3. Press `Ctrl` + `D`, then confirm when it asks to turn off OS verification.
4. The device will wipe local data and re-provision itself. This takes a few minutes, don't interrupt it.
5. From now on, every boot shows an "OS verification is off" warning screen — press `Ctrl` + `D` (or just wait ~30s) to continue booting.

Once you're in Developer Mode, `Ctrl` + `Alt` + `T` opens Crosh, and typing `shell` drops you into a real Linux shell with root access via `sudo`. That's the gate you need before doing anything below.

## Resources worth checking out

With root access unlocked, here's what people are actually doing with it:

- [Configuring 3G in Chromebook using SIM cards](http://www.techulator.com/resources/13041-How-to-configure-3G-in-Chromebook-using-SIM-cards.aspx)
- [Chromebook 4G discussion thread](https://productforums.google.com/forum/#!topic/chromebook-central/oCDcUz0XUx0)
- [Crouton](https://www.linux.com/learn/how-easily-install-ubuntu-chromebook-crouton%20) — runs a full Ubuntu chroot alongside ChromeOS, probably the most useful one of the three.
