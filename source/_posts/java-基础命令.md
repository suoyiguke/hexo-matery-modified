---
title: java-基础命令.md
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
首先确定电脑环境变量配置正确
1、直接执行class文件

进入到文件夹里，看到了HelloWorld.class文件。可以直接执行
~~~
java HelloWorld
~~~

2、运行java文件


cmd进入java文件路径下
编译成字节码.class文件 javac HelloWorld.java 
运行文件，使用-cp参数指定类文件搜索路径 java -cp D:\ajava\test HelloWorld 
