---
title: juc---Atomic原子类基本概念（一）.md
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
title: juc---Atomic原子类基本概念（一）.md
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
> 天道酬勤

我们知道，多线程并发地执行i++，因为i++操作不具备原子性，可能导致更新丢失。如A线程和B线程同时执行i++，两个线程读到的i的值都为1，均在1的基础上加1。那么经过两个线程操作之后可能i不等于3，而是等于2。

因为A和B线程在更新变量i的时候拿到的i都是1，这就是线程不安全的更新操作，通常我们会使用synchronized来解决这个问题，synchronized会保证多线程不会同时更新变量i。而Java从JDK 1.5开始提供了java.util.concurrent.atomic包 ，这个包中的原子操作类提供了一种`用法简单、性能高效、线程安全`地更新一个变量的方式。


jdk1.8下 java.util.concurrent.atomic包中有17个类，如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-61b3abcb129953bd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

它分别包括了 3个基本类型、3个数组类型、3个引用类型、3个类字段类型和 5个jdk1.8新增的原子操作类。所以总共17个原子操作类。

######基本类型的原子更新
Atomic包提供了3种基本类型的原子更新，即是：
> AtomicBoolean、AtomicInteger、AtomicLong 


######数组的原子更新
通过原子的方式更新数组里的某个元素，Atomic包提供了以下3个类：

> AtomicIntegerArray、AtomicLongArray、AtomicReferenceArray


######引用类型的原子更新
原子更新基本类型的AtomicInteger，只能更新一个变量，如果要原子更新多个变量，就需要使用这个原子更新引用类型提供的类。Atomic包提供了以下3个类：
>AtomicReference、AtomicReferenceFieldUpdater、AtomicMarkableReference

######类字段的原子更新
如果需原子地更新某个类里的某个字段时，就需要使用原子更新字段类，Atomic包提供了以下3个类进行原子字段更新：
>AtomicIntegerFieldUpdater、AtomicLongFieldUpdater、AtomicStampedReference

######分散热点的高性能原子更新
jdk1.8中引入了5个类，分别是
>Striped64、LongAdder、LongAccumulator、DoubleAdder、DoubleAccumulator

其中Striped64是抽象类，其他4个类均继承了它。它们在高并发下的性能表现优秀。如在高并发下就可使用LongAdder而不是AtomicLong

###Atomic能够保证 可见性和原子性
因为其底层是使用volatile和 CAS 实现的

1、首先使用了volatile 保证了内存可见性。
2、然后使用了CAS（compare-and-swap）算法 保证了原子性。
