---
title: jvm-《深入理解JVM-＆-G1-GC-》学习笔记之-finalize()方法和finalization-机制.md
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
title: jvm-《深入理解JVM-＆-G1-GC-》学习笔记之-finalize()方法和finalization-机制.md
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
Java 语言提供了对象终止（ finalization ） 机制来允许开发人员提供对象被销毁之前的自定义处理逻辑。 Object 类提供了 finalize 方法来添加自定义的销毁逻辑。
如果一个类有特殊的销毁逻辑，可以覆写 finalize 方法。从功能上来说， finalize 方法与 C＋＋中 的析构函数比较相似，但是 Java 采用的是基于垃圾回收器的自动内存管理机制，所以 finalize 方法在本质上不同于 C＋＋中的析构函数。当垃圾回收器发现没有引用指向一个对象时 ， 会调用这个对象的 finalize 方法。通常在这个方法中进行一些资源释放和清理的工作，比如关闭文件、套接字和数据库连接等 。

由于 finalize 方法的存在，虚拟机中的对象一般处于三种可能的状态。

###finalize 方法将对象分为三种状态
######第一种是可达状态
当有引用指向该对象时，该对象处于可达状态。
根据引用类型的不同，有可能处于`强引用可达`、`软引用可达`或`弱引用可达`状态。

######第二种是可复活状态

如果对象的类覆写了 finalize 方法，则对象有可能处于该状态。虽然垃圾回收器是在对象没有引用的情况下才调用其 finalize 方法，但是在 finalize 方法的实现中可能为当前对象添加新的引用。因此在 finalize 方法运行完成之后，垃圾回收器需要重新检查该对象的引用。如果发现新的引用，那么对象会回到可达状态，相当于该对象被复活，否则对象会变成不可达状态。当对象从可复活状态变为可达状态之后，对象会再次出现没有引用存在的情况。在这个情况下， finalize 方法不会被再次调用，对象会直接变成不可达状态， 也就是说，一个对象的 finalize 方法只会被调用一次。 

######第三种是不可达状态
在这个状态下，垃圾回收器可以自由地释放对象所占用的内存空间。

 
######理解
从原文中可以理解到
>-  在对象没有引用的情况下才调用 方法
> - finalize 方法中可以进行一些资源释放和清理的工作，比如关闭文件、套接字和数据库连接等 。
>- finalize方法只会执行一次
>- 若重写finalize方法，可能导致对象复活
