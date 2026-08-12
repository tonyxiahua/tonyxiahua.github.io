---
title: "Windows To Go on Macbook"
date: 2016-11-09 07:00:04
categories:
  - 技术
---

## 介绍

Macbook的用户难免会有Windows 的需求，然而又不想划分一块宝贵的SSD 空间给没什么卵用的微软。那该怎么办呢？ 下面就用我的电脑来做示范，mid-2014 的 Macbook Pro 13 Retina 配合使用U盘进行Windows To Go 搭建Windows 环境（非虚拟机）。  
<!-- more -->

## 准备资源

你需要准备以下这些材料，才能保证操作顺利进行：

- 一个至少32GB、读写速度足够快的USB 3.0 U盘（强烈建议用USB 3.0接口，USB 2.0速度太慢，用起来会很难受）
- 一份Windows 10 Enterprise 镜像，Windows To Go 官方只支持企业版
- Windows 企业版自带的Windows To Go Creator 工具，或者用Rufus这类第三方工具
- 一台能正常从U盘启动的Macbook（Boot Camp 或者EFI引导都可以）

## 制作启动盘

材料备齐之后，制作过程其实很简单：

1. 在一台 Windows 电脑上打开 Windows To Go Creator（企业版自带，路径在控制面板 -> Windows To Go），或者用 Rufus 也行
2. 选择你的 U 盘和 Windows 10 Enterprise 镜像
3. 一路默认设置往下走，工具会自动分区、写入系统文件，等进度条跑完就行，U 盘越慢这一步越煎熬

## 在 Macbook 上启动

U 盘做好之后插到 Macbook 上：

1. 开机的时候按住 `Option`（Alt）键，进入启动盘选择界面
2. 选择那个 U 盘（EFI Boot 或者标着 Windows 的那个选项）
3. 正常情况下会直接进入 Windows 的安装/首次配置流程，跟着走完就能进桌面了

Macbook 的硬件驱动（触控板、Wi-Fi、显卡这些）Windows 10 不一定全都自带，进系统之后建议用 Boot Camp 助理生成一份驱动包，装上之后触控板和 Wi-Fi 基本就都正常了。速度取决于 U 盘本身的读写速度，用 USB 3.0 的高速盘体验会比普通 U 盘好很多。
