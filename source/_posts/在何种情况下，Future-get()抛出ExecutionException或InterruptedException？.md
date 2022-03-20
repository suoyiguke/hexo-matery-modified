---
title: 在何种情况下，Future-get()抛出ExecutionException或InterruptedException？.md
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
ExecutionException和InterruptedException是两个非常不同的事情。

ExecutionException封装了正在执行的线程抛出的任何异常，所以如果你的线程是做某种IO导致抛出IOException异常的，那么它会被包装在一个ExecutionException中并被重新抛出。

InterruptedException不是任何出错的迹象。在那里给你一种让你的线程知道什么时候停止的方法，以便他们完成当前的工作并优雅地退出。假设我希望我的应用程序停止运行，但我不希望我的线程放弃他们正在做的事情（这是如果我让它们守护进程线程会发生什么）。因此，当应用程序正在关闭时，我的代码会在这些线程上调用中断方法，这些线程会在中断标志上设置中断标志，并在下一次线程处于等待或休眠状态时检查中断标志并引发InterruptedException，我可以使用它从线程参与的无限循环处理/休眠逻辑中解脱出来（如果线程不等待或休眠，它可以定期检查中断标志。）因此，它是一个用于更改逻辑流程的异常实例。记录它的唯一原因是在一个示例程序中向您展示发生了什么，或者如果您正在调试中断逻辑无法正常工作的问题。
