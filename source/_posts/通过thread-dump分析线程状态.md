---
title: 通过thread-dump分析线程状态.md
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
title: 通过thread-dump分析线程状态.md
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
除了上述的分析，大多数情况下会基于thead dump分析当前各个线程的运行情况，如是否存在[死锁](https://so.csdn.net/so/search?q=%E6%AD%BB%E9%94%81&spm=1001.2101.3001.7020)、是否存在一个线程长时间持有锁不放等等。

在dump中，线程一般存在如下几种状态：
1、RUNNABLE，线程处于执行中
2、BLOCKED，线程被阻塞
3、WAITING，线程正在等待

实例1：多线程竞争synchronized锁

![image](https://upload-images.jianshu.io/upload_images/13965490-6157ac85d209f854?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

很明显：线程1获取到锁，处于RUNNABLE状态，线程2处于BLOCK状态
1、`locked <0x000000076bf62208>`说明线程1对地址为0x000000076bf62208对象进行了加锁；
2、`waiting to lock <0x000000076bf62208>` 说明线程2在等待地址为0x000000076bf62208对象上的锁；
3、`waiting for monitor entry [0x000000001e21f000]`说明线程1是通过synchronized关键字进入了监视器的临界区，并处于"Entry Set"队列，等待monitor，具体实现可以参考[深入分析synchronized的JVM实现](http://www.jianshu.com/p/c5058b6fe8e5)；
