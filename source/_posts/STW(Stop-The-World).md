---
title: STW(Stop-The-World).md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: JAVA-GC
categories: JAVA-GC
---
---
title: STW(Stop-The-World).md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: JAVA-GC
categories: JAVA-GC
---
很容易想到 Java 应用的 STW(Stop The World)，其中，特别是垃圾回收会导致短暂的应用停顿，无法响应请求。

排查垃圾回收问题第一件事自然是打开垃圾回收日志（GC log），GC log 打印了 GC 发生的时间，GC 的类型，以及 GC 耗费的时间等。增加 JVM 启动参数
~~~
-XX:+PrintGCDetails 
-Xloggc:${APPLICATION_LOG_DIR}/gc.log
-XX:+PrintGCDateStamps 
-XX:+PrintGCApplicationStoppedTime
~~~

为了方便排查，同时打印了所有应用的停顿时间。（除了垃圾回收会导致应用停顿，还有很多操作也会导致停顿，比如取消偏向锁等操作）。由于应用是在 docker 环境，因此每次应用发布都会导致 GC 日志被清除，写了个上报程序，定时把 GC log 上报到 elk 平台，方便观察。

以下是接口超时时 GC 的情况：

![图片](https://upload-images.jianshu.io/upload_images/13965490-acc9e7d1bfa6781b?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看到，有次 GC 耗费的时间接近两秒，应用的停顿时间也接近两秒，而且此次的垃圾回收是 ParNew 算法，也就是发生在新生代。所以基本可以确定，**是垃圾回收的停顿导致应用不可用，进而导致接口超时**。
