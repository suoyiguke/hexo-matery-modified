---
title: JAVA-垃圾回收之强、软、弱、虚引用（一）.md
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
title: JAVA-垃圾回收之强、软、弱、虚引用（一）.md
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
>自助者天助之

Java 中提供了 4 个级别的引用，即强引用（ Strong Reference ）、软引用（Soft Reference）、弱引用（ Weak Reference ）、虚引用（ Phantom Reference ）这 4 个级别 。

在这 4 个级别中只有强引用类是包内可见的，其他 3 种引用类型均为 Public，可以在应用程序中直接使用，垃圾回收器会尝试回收只有弱引用的对象。


简要罗列一个 GC 对于不同引用类型的区别。

######强引用

在一个线程内，无需引用直接可以使用的对象，除非引用不存在了，否则强引用不会被 GC 清理。我们平时声明变量使用的就是强引用，普通系统 99%以上都是强引用，比如， Strings ＝”Hello World” 。
强引用具体的特征和用法，可以看看这篇：https://www.jianshu.com/p/83998024c751

######软引用
 JVM 抛出 OOM 之前， GC 清理所有的软引用对象。垃圾回收器在某个时刻决定回收软可达的对象的时候，会清理软引用，并可选地把引用存放到一个引用队列（ Reference Queue)  类似弱引用，只不过 Java 虚拟机会尽量让软引用的存活时间长一些，迫不得已才清理。
软引用具体的特征和用法，可以看看这篇：
https://www.jianshu.com/p/353d515d7b23

######弱引用
 弱引用对象与软引用对象的最大不同就在于，当 GC 在
进行回收时 ，需要通过算法检查是否回收软引用对象，而对于弱引用对象， GC 总是进行回收。弱 引 用对象更容易 、 更快被 GC 回收。虽然， GC 在运行时一定回收弱引用对象 ， 但是复杂关系 的弱对象群常常需要好几次 GC 的运行才能完成。就像上面描述的场景 ， 弱引用对象常常用于 Map 结构中，引用数据量较大的对象，一旦该对象的强引用为 null 时 ， GC 能够快速地回收该对象空间。
弱引用具体的特征和用法，可以看看这篇： https://www.jianshu.com/p/bcfbecc4d12f


######虚引用
又称为幽灵引用，主要目的是在一个对象所占的内存被实际回收之前得到通知， 从而可以进行一些相关的清理工作。幽灵引用在使用方式上与之前介绍的三种引用类型有很大的不同。首先幽灵引用在创建时必须提供一个引用队列作为参数，其次幽灵引用对象的 get 方法总是返回 null ， 因此无法通过幽灵引用来获取被引用 的对象。

