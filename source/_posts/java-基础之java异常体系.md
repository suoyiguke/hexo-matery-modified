---
title: java-基础之java异常体系.md
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
#Java异常类的架构
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d66aae69de2722b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




### RuntimeException/UnCheckException

定义: RuntimeException及其子类都被称为运行时异常。
特点: Java编译器不会检查它。也就是说，当程序中可能出现这类异常时，倘若既"没有通过throws声明抛出它"，也"没有用try-catch语句捕获它"，还是会编译通过。
spring框架的@Transactional事务注解默认回滚RuntimeException。


例如，除数为零时产生的ArithmeticException异常，数组越界时产生的IndexOutOfBoundsException异常，fail-fail机制产生的ConcurrentModificationException异常、常见的空指针异常NullPointerException等，都属于运行时异常。

虽然Java编译器不会检查运行时异常，但是我们也可以通过throws进行声明抛出，也可以通过try-catch对它进行捕获处理。
>如果产生运行时异常，则需要通过修改代码来进行避免。例如，若会发生除数为零的情况，则需要通过代码避免该情况的发生！

### CheckException

定义: Exception类本身，以及Exception的子类中除了"运行时异常"之外的其它子类都属于被检查异常。
特点: Java编译器会检查它。此类异常，要么通过throws进行声明抛出，要么通过try-catch进行捕获处理，否则不能通过编译。例如进行文件操作时遇到的IOException、线程sleep方法/obj的wait方法抛出的InterruptedException等都属于CheckException。

@Transactional事务注解默认不会回滚checkException，需要指定Exception父类，用法如下：
@Transactional(rollbackFor = Exception.class); 而且捕获后需要抛出给上层调用者，这样事务才会正常回滚。


>被检查异常通常都是可以恢复的。

### ERROR
定义: Error类及其子类。
特点: 和运行时异常一样，编译器也不会对错误进行检查。
当资源不足、约束失败、或是其它程序无法继续运行的条件发生时，就产生错误。程序本身无法修复这些错误的。例如，VirtualMachineError就属于错误。

@Transactional事务注解默认回滚ERROR

例如我们常见的虚拟机内存栈溢出错误StackOverflowError。


> 熟悉java异常机制对我们使用spring声明式事务有很大帮助！这篇文章探讨了异常和spring事务的关系 https://www.jianshu.com/p/702ac5630b99
