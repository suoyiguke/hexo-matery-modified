---
title: juc---线程池之工作原理.md
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
title: juc---线程池之工作原理.md
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
######线程池原理示意
这张图已经完全概括了线程池的工作流程，其中1,2,3,4 就是执行步骤
![image.png](https://upload-images.jianshu.io/upload_images/13965490-cfbc00135a2cc09e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######线程池内部对新提交的任务处理流程图
![image.png](https://upload-images.jianshu.io/upload_images/13965490-08e508c41d91e080.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###原理描述
step1、在创建了线程池后，开始等待请求。

step2、当调用execute()方法添加一个请求任务时，线程池会做出如下判断：
  ①、如果正在运行的线程数量小于corePoolSize，那么马上创建线程运行这个任务；
  ②、如果正在运行的线程数量大于或等于corePoolSize，那么将这个任务放入队列；
  ③、如果这个时候队列满了且正在运行的线程数量还小于maximumPoolSize，那么还是要创建非核心线程立刻运行这个任务；
  ④、如果队列满了且正在运行的线程数量大于或等于maximumPoolSize，那么线程池会启动饱和拒绝策略来执行。

step3、当一个线程完成任务时，它会从队列中取下一个任务来执行。

step4、当一个线程无事可做超过一定的时间（keepAliveTime）时，线程会判断：
    如果当前运行的线程数大于corePoolSize，那么这个线程就被停掉。
    所以线程池的所有任务完成后，它最终会收缩到corePoolSize的大小。
