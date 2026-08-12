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
