---
title: jmm-java内存模型.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jmm
categories: jmm
---
---
title: jmm-java内存模型.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jmm
categories: jmm
---
###什么是JMM
- JMM定义了Java 虚拟机(JVM)在计算机内存(RAM)中的工作方式。
- JVM是整个计算机虚拟模型，所以JMM是隶属于JVM的。
- 从抽象的角度来看，JMM定义了线程和主内存之间的抽象关系：线程之间的共享变量存储在`主内存（Main Memory）`中，每个线程都有一个`私有的本地内存（Local Memory）`，本地内存中存储了该线程以读/写共享变量的副本。

- 本地内存是JMM的一个抽象概念，并不真实存在。它涵盖了缓存、写缓冲区、寄存器以及其他的硬件和编译器优化。





###主内存和工作内存

![image.png](https://upload-images.jianshu.io/upload_images/13965490-434a53c57debc756.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###JMM的关键问题
`两大核心,三条性质`
- 两大核心：JMM内存模型（主内存和工作内存）以及happens-before；
- 三条性质：原子性，可见性，有序性。

###JVM对Java内存模型的实现

*   在JVM内部，Java内存模型把内存分成了两部分：线程栈区和堆区
    JVM中运行的每个线程都拥有自己的线程栈，线程栈包含了当前线程执行的方法调用相关信息，我们也把它称作调用栈。随着代码的不断执行，调用栈会不断变化。

- 所有原始类型(boolean,byte,short,char,int,long,float,double)的局部变量都直接保存在线程栈当中，对于它们的值各个线程之间都是独立的。对于原始类型的局部变量，一个线程可以传递一个副本给另一个线程，当它们之间是无法共享的。

- 堆区包含了Java应用创建的所有对象信息，不管对象是哪个线程创建的，其中的对象包括原始类型的封装类（如Byte、Integer、Long等等）。不管对象是属于一个成员变量还是方法中的局部变量，它都会被存储在堆区。
- 一个局部变量如果是原始类型，那么它会被完全存储到栈区。 一个局部变量也有可能是一个对象的引用，这种情况下，这个本地引用会被存储到栈中，但是对象本身仍然存储在堆区。

- 对于一个对象的成员方法，这些方法中包含局部变量，仍需要存储在栈区，即使它们所属的对象在堆区。

- 对于一个对象的成员变量，不管它是原始类型还是包装类型，都会被存储到堆区。Static类型的变量以及类本身相关信息都会随着类本身存储在堆区。

![image](//upload-images.jianshu.io/upload_images/4222138-1cc1cd7e5e09232c.png?imageMogr2/auto-orient/strip|imageView2/2/w/486/format/webp)

