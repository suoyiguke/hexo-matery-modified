---
title: jvm介绍.md
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
title: jvm介绍.md
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
###什么是JVM
Java程序的跨平台特性主要是指字节码文件可以在任何具有Java虚拟机的计算机或者电子设备上运行，Java虚拟机中的Java解释器负责将字节码文件解释成为特定的机器码进行运行。因此在运行时，Java源程序需要通过编译器编译成为.class文件。众所周知java.exe是java class文件的执行程序，但实际上java.exe程序只是一个执行的外壳，它会装载jvm.dll（windows下，下皆以windows平台为例，linux下和solaris下其实类似，为：libjvm.so），这个动态连接库才是java虚拟机的实际操作处理所在。

JVM是JRE的一部分。它是一个虚构出来的计算机，是通过在实际的计算机上仿真模拟各种计算机功能来实现的。JVM有自己完善的硬件架构，如处理器、堆栈、寄存器等，还具有相应的指令系统。Java语言最重要的特点就是跨平台运行。使用JVM就是为了支持与操作系统无关，实现跨平台。所以，JAVA虚拟机JVM是属于JRE的，而现在我们安装JDK时也附带安装了JRE(当然也可以单独安装JRE)。


###JVM和操作系统的关系
JVM是运行在操作系统之上的，它与硬件没有直接的交互
![image.png](https://upload-images.jianshu.io/upload_images/13965490-feac6784486ede7a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###JVM体系结构
Java 的设计理念是 WORA`（Write Once Run Anywhere,一次编写到处运行）`。编译器将 Java 文件编译为 Java .class 文件，然后将 .class 文件输入到 JVM 中，JVM 执行类文件的加载和执行，最后转变成机器可以识别的机器码进行最终的操作。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a57f1d45a0d1d770.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




