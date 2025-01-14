---
title: jvm-《深入理解Java虚拟机》学习笔记之程序计数器.md
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
title: jvm-《深入理解Java虚拟机》学习笔记之程序计数器.md
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
程序计数器（Program Counter Register） 是一块较小的内存空间， 它可以看作是当前线程所执行的字节码的行号指示器。 在Java虚拟机的概念模型里[1]， 字节码解释器工作时就是通过改变这个计数器的值来选取下一条需要执行的字节码指令， 它是程序控制流的指示器， 分支、 循环、 跳转、 异常处理、 线程恢复等基础功能都需要依赖这个计数器来完成。由于Java虚拟机的多线程是通过线程轮流切换、 分配处理器执行时间的方式来实现的， 在任何一个确定的时刻， 一个处理器（对于多核处理器来说是一个内核） 都只会执行一条线程中的指令。 因此， 为了线程切换后能恢复到正确的执行位置， 每条线程都需要有一个独立的程序计数器， 各条线程之间计数器互不影响， 独立存储， 我们称这类内存区域为“线程私有”的内存。如果线程正在执行的是一个Java方法， 这个计数器记录的是正在执行的虚拟机字节码指令的地址； 如果正在执行的是本地（Native） 方法， 这个计数器值则应为空（Undefined） 。 此内存区域是唯一一个在《Java虚拟机规范》 中没有规定任何OutOfMemoryError情况的区域。[1] “概念模型”这个词会经常被提及， 它代表了所有虚拟机的统一外观， 但各款具体的Java虚拟机并不一定要完全照着概念模型的定义来进行设计， 可能会通过一些更高效率的等价方式去实现它。

###总结
- 程序计数器 完成程序控制流的指示器， 分支、 循环、 跳转、 异常处理、 线程恢复等基础功能
- 线程私有
- JVM规范中唯一没有规定OutOfMemoryError情况的区域
- 如果正在执行的是Native 方法，则这个计数器值为空
