---
title: java-查看汇编指令.md
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
1、idea运行配置
~~~
-XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly 
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6127507629f26b29.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2、将hsdis-amd64.dll文件放到\jdk1.8\jre\bin下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fe2af406d548fcdd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

3、运行即可
![image.png](https://upload-images.jianshu.io/upload_images/13965490-6f09f4849643d5b5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
