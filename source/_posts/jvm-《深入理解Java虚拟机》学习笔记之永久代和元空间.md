---
title: jvm-《深入理解Java虚拟机》学习笔记之永久代和元空间.md
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
title: jvm-《深入理解Java虚拟机》学习笔记之永久代和元空间.md
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
###PermGen 永久代

说到方法区， 不得不提一下“永久代”这个概念， 尤其是在JDK 8以前， 许多Java程序员都习惯在HotSpot虚拟机上开发、 部署程序， 很多人都更愿意把方法区称呼为“永久代”（PermanentGeneration） ， 或将两者混为一谈。 本质上这两者并不是等价的， 因为仅仅是当时的HotSpot虚拟机设计团队选择把收集器的分代设计扩展至方法区， 或者说使用永久代来实现方法区而已， 这样使得HotSpot的垃圾收集器能够像管理Java堆一样管理这部分内存， 省去专门为方法区编写内存管理代码的工作。 但是对于其他虚拟机实现， 譬如BEA JRockit、 IBM J9等来说， 是不存在永久代的概念的。 原则上如何实现方法区属于虚拟机实现细节， 不受《Java虚拟机规范》 管束， 并不要求统一。 但现在回头来看， 当年使用永久代来实现方法区的决定并不是一个好主意， 这种设计导致了Java应用更容易遇到内存溢出的问题（永久代有-XX： MaxPermSize的上限， 即使不设置也有默认大小， 而J9和JRockit只要没有触碰到进程可用内存的上限， 例如32位系统中的4GB限制， 就不会出问题） ， 而且有极少数方法（例如String::intern()） 会因永久代的原因而导致不同虚拟机下有不同的表现。 当Oracle收购BEA获得了JRockit的所有权后， 准备把JRockit中的优秀功能， 譬如Java Mission Control管理工具， 移植到HotSpot虚拟机时， 但因为两者对方法区实现的差异而面临诸多困难。 考虑到HotSpot未来的发展， 在JDK 6的时候HotSpot开发团队就有放弃永久代， 逐步改为采用本地内存（Native Memory） 来实现方法区的计划了[1]， 到了JDK 7的HotSpot， 已经把原本放在永久代的字符串常量池、 静态变量等移出， 而到了JDK 8， 终于完全废弃了永久代的概念， 改用与JRockit、 J9一样在本地内存中实现的元空间（Metaspace） 来代替， 把JDK 7中永久代还剩余的内容（主要是类型信息） 全部移到元空间中。






###Metaspace 元空间


从JDK8开始，永久代(PermGen)的概念被废弃掉了，取而代之的是一个称为Metaspace的存储空间。

Metaspace使用的是本地内存，而不是堆内存，`也就是说在默认情况下Metaspace的大小只与本地内存大小有关`。


###方法区和 永久代、 元空间之间的关系

方法区是 JVM 的规范（可以把方法区看成一个接口），而永久代、 元空间则是 JVM 规范的一种实现，并且只有 HotSpot 才有 “PermGen space”，而对于其他类型的虚拟机，如 JRockit（Oracle）、J9（IBM） 并没有“PermGen space”。

永久代是JDK6中方法区的实现、元空间则是JDK7、JDK8中方法区的实现


###总结


1、jdk7 时把原本放在永久代的符号引用(Symbols)转移到了native heap；字面量/字符串常量池(interned strings)转移到了java heap；类的静态变量(class statics)转移到了java heap

2、永久代在jdk8时被完全废弃，使用在本地内存中实现的 `元空间`（Metaspace） 来代替， 把JDK 7中永久代还剩余的内容（主要是类型信息） 全部移到元空间中

3、元空间的本质和永久代类似，都是对JVM规范中方法区的实现。不过元空间与永久代之间最大的区别在于：`元空间并不在虚拟机中，而是使用本地内存`。因此，默认情况下，元空间的大小仅受本地内存限制
