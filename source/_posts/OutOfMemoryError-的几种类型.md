---
title: OutOfMemoryError-的几种类型.md
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
title: OutOfMemoryError-的几种类型.md
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
Become OOM Killer
我们都知道JVM的内存管理是自动化的，Java语言的程序指针也不需要开发人员手工释放，JVM的GC会自动的进行回收，但是，如果编程不当，JVM仍然会发生内存泄露，导致Java程序产生了OutOfMemoryError（OOM）错误。

产生OutOfMemoryError错误的原因包括：

>java.lang.OutOfMemoryError: Java heap space
java.lang.OutOfMemoryError: PermGen space及其解决方法
java.lang.OutOfMemoryError: unable to create new native thread
java.lang.OutOfMemoryError：GC overhead limit exceeded

1、对于第1种异常，表示Java堆空间不够，当应用程序申请更多的内存，而Java堆内存已经无法满足应用程序对内存的需要，将抛出这种异常。

2、对于第2种异常，表示Java永久带（方法区）空间不够，永久带用于存放类的字节码和长常量池，类的字节码加载后存放在这个区域，这和存放对象实例的堆区是不同的，大多数JVM的实现都不会对永久带进行垃圾回收，因此，只要类加载的过多就会出现这个问题。一般的应用程序都不会产生这个错误，然而，对于Web服务器来讲，会产生有大量的JSP，JSP在运行时被动态的编译成Java Servlet类，然后加载到方法区，因此，太多的JSP的Web工程可能产生这个异常。

3、对于第3种异常，本质原因是创建了太多的线程，而能创建的线程数是有限制的，导致了这种异常的发生。

4、对于第4种异常，是在并行或者并发回收器在GC回收时间过长、超过98%的时间用来做GC并且回收了不到2%的堆内存，然后抛出这种异常进行提前预警，用来避免内存过小造成应用不能正常工作。

####unable to create new native thread
到现在为止，从现象的规律上我们已经没法继续分析下去了，那我们回顾一下错误本身：

java.lang.OutOfMemoryError: unable to create new native thread

顾名思义，错误产生的原因就是应用不能创建线程了，但是，应用还需要创建线程。为什么程序不能创建线程呢？

有两个具体原因造成这个异常:

由于线程使用的资源过多，操作系统已经不能再提供给应用资源了。
操作系统设置了应用创建线程的最大数量，并且已经达到了最大允许数量。
上面第1条资源指的是内存，而第2条中，在Linux下线程使用轻量级进程实现的，因此线程的最大数量也是操作系统允许的进程的最大数量。

###下面两个异常与OOM有关系，但是，又没有绝对关系。
java.lang.StackOverflowError ...
java.net.SocketException: Too many open files
对于第1种异常，是JVM的线程由于递归或者方法调用层次太多，占满了线程堆栈而导致的，线程堆栈默认大小为1M。

对于第2种异常，是由于系统对文件句柄的使用是有限制的，而某个应用程序使用的文件句柄超过了这个限制，就会导致这个问题。
定位和解决的过程。
