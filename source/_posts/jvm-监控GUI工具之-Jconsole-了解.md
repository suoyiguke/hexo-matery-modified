---
title: jvm-监控GUI工具之-Jconsole-了解.md
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
title: jvm-监控GUI工具之-Jconsole-了解.md
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
[toc]

## [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#jvm%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-gui%E7%AF%87)JVM监控及诊断工具-GUI篇

很多JDK自带的GUI工具都在bin目录下

### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#jconsole-%E4%BA%86%E8%A7%A3)Jconsole 了解

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E5%90%AF%E5%8A%A8)启动

![image-20210518235707000](https://upload-images.jianshu.io/upload_images/13965490-7c1679cffdb2958b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E8%BF%9E%E6%8E%A5)连接

![image-20210519000148496](https://upload-images.jianshu.io/upload_images/13965490-b3da30b3a175a001.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

无法连接解决方案,启动JVM参数加上

<pre style="box-sizing: border-box; overflow: auto; font-family: SFMono-Regular, Menlo, Monaco, Consolas, &quot;Liberation Mono&quot;, &quot;Courier New&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; line-height: 1.45; background-color: rgb(246, 248, 250); border-radius: 3px; word-break: normal; min-height: 52px; tab-size: 4; color: rgb(51, 51, 51);">-Dcom.sun.management.jmxremote 
-Dcom.sun.management.jmxremote.port=8011 
-Dcom.sun.management.jmxremote.ssl=false
-Dcom.sun.management.jmxremote.authenticate=false</pre>

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E6%9F%A5%E7%9C%8B%E4%BF%A1%E6%81%AF)查看信息

> 概述信息

![image-20210519000756518](https://upload-images.jianshu.io/upload_images/13965490-415df624cb6adc4d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 内存信息

![image-20210519000816175](https://upload-images.jianshu.io/upload_images/13965490-9438efc012c88ec1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 线程信息 可检查死锁

![image-20210519000835395](https://upload-images.jianshu.io/upload_images/13965490-f58766e0041a79e6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 关于类信息

![image-20210519000848394](https://upload-images.jianshu.io/upload_images/13965490-2b1cd5a570f77ea1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> 有关VM以及参数等信息

![image-20210519000900135](https://upload-images.jianshu.io/upload_images/13965490-fa96d5edc385c65e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

