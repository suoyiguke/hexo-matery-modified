---
title: juc---StampedLock.md
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
title: juc---StampedLock.md
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
StampedLock 读音 [stæmptlɑːk]

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7dd060c8461b3e17.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



- StampedLock 是从 JDK1.8 开始提供，它的性能比 ReadWriteLock 好

- StampedLock 支持：乐观读锁、悲观读锁、写锁

- StampedLock 的悲观读锁、写锁，与 ReadWriteLock 的读锁、写锁用法相似：读读可并行、读写互斥、写写互斥。

- StampedLock 之所以性能优于 ReadWriteLock，因为它支持乐观读锁。乐观读锁操作，支持一个线程并发进行写操作。

- StampedLock 不支持重入

- StampedLock 支持锁的降级和升级

- StampedLock 可以用悲观读锁调用 readLockInterruptibly() 方法和写锁调用 writeLockInterruptibly() 方法，支持可中断
