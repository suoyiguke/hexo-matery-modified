---
title: java阻塞队列.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
---
title: java阻塞队列.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
1、下面关于阻塞队列（java.util.concurrent.BlockingQueue）的说法不正确的是 D
A. 阻塞队列是线程安全的 
B. 阻塞队列的主要应用场景是“生产者-消费者”模型 
C. 阻塞队列里的元素不能为null 
D. 阻塞队列的实现必须显示地设置容量 

分析：在ArrayBlockQueue里有这个非空判断，故C正确
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8be547a16f2933b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

D 错误， ArrayBlockQueue的确是要显示的设置初始化容量，但是同样为阻塞队列的SynchronousQueue容量就是1，不能设置容量

![image.png](https://upload-images.jianshu.io/upload_images/13965490-420d70d764e60f23.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/13965490-6d29d4267bfc94f8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
