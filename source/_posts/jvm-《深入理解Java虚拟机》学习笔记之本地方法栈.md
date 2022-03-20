---
title: jvm-《深入理解Java虚拟机》学习笔记之本地方法栈.md
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
title: jvm-《深入理解Java虚拟机》学习笔记之本地方法栈.md
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
本地方法栈（Native Method Stacks） 与虚拟机栈所发挥的作用是非常相似的， 其区别只是虚拟机栈为虚拟机执行Java方法（也就是字节码） 服务， `而本地方法栈则是为虚拟机使用到的本（Native）方法服务。`



《Java虚拟机规范》 对本地方法栈中方法使用的语言、 使用方式与数据结构并没有任何强制规定， 因此具体的虚拟机可以根据需要自由实现它， 甚至有的Java虚拟机（譬如Hot-Spot虚拟机） 直接
就把本地方法栈和虚拟机栈合二为一。 与虚拟机栈一样， 本地方法栈也会在栈深度溢出或者栈扩展失败时分别抛出StackOverflowError和OutOfMemoryError异常。
