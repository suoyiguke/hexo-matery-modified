---
title: 兼容windows和linux的磁盘路径写法.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
这样写
  String path = File.separator + "home" + File.separator + "file" + File.separator;
