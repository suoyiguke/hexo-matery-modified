---
title: jvm-jvisualvm工具的使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
---
title: jvm-jvisualvm工具的使用.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
这个工具的文件路径 jdk1.8\bin\jvisualvm.exe

visualvm.exe.可以用来分析堆内存快照
出现java.lang.OutOfMemoryError: Java heap space堆内存溢出时需要定位bug位置，就可以使用这个工具来分析了



打开堆快照的.hppof文件

查看堆内存中最多数量的实例


出现堆内存溢出的代码位置


###在使用 jvisualvm 分析大的 dump 文件时，堆查器使用的内存不足

修改 JAVA_HOME/lib/visualvm/etc/visualvm.conf 文件中 visualvm_default_options="-J-client -J-Xms24 -J-Xmx256m"，然后重启 jvisualVM 即可
