---
title: java-我见过的异常.md
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
1、在对ArrayList并发add时报出
并发修改异常
java.util.ConcurrentModificationException 

2、
BrokenBarrierException异常

3、IllegalTransactionStateException异常
事务的传播行为出现的异常

4、线程中断异常
InterruptedException

5、线程池拒绝策略异常
java.util.concurrent.RejectedExecutionException


###错误


SO 栈内存溢出 错误
 java.lang.StackOverflowError
>StackOverflowError extends VirtualMachineError

OOM 堆内存溢出 错误
java.lang.OutOfMemoryError
> OutOfMemoryError extends VirtualMachineError 
