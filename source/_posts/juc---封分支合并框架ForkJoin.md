---
title: juc---封分支合并框架ForkJoin.md
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
title: juc---封分支合并框架ForkJoin.md
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
###分支合并示意图
![image.png](https://upload-images.jianshu.io/upload_images/13965490-df90a5d8136bfcb0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###Fork和Join
Fork：把一个复杂任务进行分拆，大事化小
Join：把分拆任务的结果进行合并


###ForkJoinPool
ForkJoinPool类继承自AbstractExecutorService，而AbstractExecutorService实现了ExecutorService接口。也就是说ForkJoinPool拥有线程池的功能
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1f634c5929ae6b82.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###ForkJoinTask
ForkJoinTask实现了Future接口。ForkJoinTask可以类比线程池中的FutureTask
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0dec7d2692e6ac32.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
