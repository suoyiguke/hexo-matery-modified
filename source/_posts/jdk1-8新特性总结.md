---
title: jdk1-8新特性总结.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
https://gitee.com/SnailClimb/JavaGuide/blob/master/docs/java/new-features/Java8%E6%96%B0%E7%89%B9%E6%80%A7%E6%80%BB%E7%BB%93.md#localdatetime%E6%9C%AC%E5%9C%B0%E6%97%A5%E6%9C%9F%E6%97%B6%E9%97%B4

Oracle 于 2014 发布了 Java8（jdk1.8），诸多原因使它成为目前市场上使用最多的 jdk 版本。虽然发布距今已将近 7 年，但很多程序员对其新特性还是不够了解，尤其是用惯了 java8 之前版本的老程序员，比如我。

为了不脱离队伍太远，还是有必要对这些新特性做一些总结梳理。它较 jdk.7 有很多变化或者说是优化，比如 interface 里可以有静态方法，并且可以有方法体，这一点就颠覆了之前的认知；`java.util.HashMap` 数据结构里增加了红黑树；还有众所周知的 Lambda 表达式等等。本文不能把所有的新特性都给大家一一分享，只列出比较常用的新特性给大家做详细讲解。更多相关内容请看[官网关于 Java8 的新特性的介绍](https://www.oracle.com/java/technologies/javase/8-whats-new.html)。



Interface & functional Interface
Lambda
Stream
Optional
Date time-api
这些都是开发当中比较常用的特征。梳理下来发现它们真香，而我却没有更早的应用。总觉得学习 java 8 新特性比较麻烦，一致使用老的实现方式。其实这些新特性几天就可以掌握，一但掌握，效率会有很大的提高。其实我们涨工资也是涨的学习的钱，不学习终究会被淘汰，35 岁危机会提前来临。
