---
title: java基本数据类型.md
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
Java 中的几种基本数据类型是什么？对应的包装类型是什么？各自占用多少字节呢？
Java 中有 8 种基本数据类型，分别为：

6 种数字类型 ：byte、short、int、long、float、double
1 种字符类型：char
1 种布尔型：boolean。
这 8 种基本数据类型的默认值以及所占空间的大小如下：

基本类型	位数	字节	默认值
int	32   	4	0
short	16	2	0
long	64	8	0L
byte	8	1	0
char	16	2	'u0000'
float	32	4	0f
double	64	8	0d
boolean	1		false

另外，对于 boolean，官方文档未明确定义，它依赖于 JVM 厂商的具体实现。逻辑上理解是占用 1 位，但是实际中会考虑计算机高效存储因素。

注意：

1、ava 里使用 long 类型的数据一定要在数值后面加上 L，否则将作为整型解析。
2、char a = 'h'char :单引号，String a = "hello" :双引号。

这八种基本类型都有对应的包装类分别为：Byte、Short、Integer、Long、Float、Double、Character、Boolean 。

包装类型不赋值就是 Null ，而基本类型有默认值且不是 Null。

另外，这个问题建议还可以先从 JVM 层面来分析。

基本数据类型直接存放在 Java 虚拟机栈中的局部变量表中，而包装类型属于对象类型，我们知道对象实例都存在于堆中。相比于对象类型， 基本数据类型占用的空间非常小。

《深入理解 Java 虚拟机》 ：局部变量表主要存放了编译期可知的基本数据类型**（boolean、byte、char、short、int、float、long、double）**、对象引用（reference 类型，它不同于对象本身，可能是一个指向对象起始地址的引用指针，也可能是指向一个代表对象的句柄或其他与此对象相关的位置）。
