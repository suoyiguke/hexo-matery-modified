---
title: jmm-synchronized的内存语义和它是如何保证并发三大特性的.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jmm
categories: jmm
---
---
title: jmm-synchronized的内存语义和它是如何保证并发三大特性的.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jmm
categories: jmm
---

###synchronized实现可见性

jmm中的`happens-before规则`中有一条`监视器规则`：对同一个监视器的解锁，happens-before于对该监视器的加锁

1、线程解锁前，必须把工作内存中共享变量的最新值刷新到主内存中
2、线程加锁时，将清空工作内存中共享变量的值，从而使用共享变量时需要从主内存中重新获取最新的值`（注意：加锁与解锁需要是同一把锁）`

happens-before规则，我的这篇文章中有提到
https://www.jianshu.com/p/bb894b1fe2e6


###synchronized实现原子性
synchronized实现原子性需要`多个线程之间使用相同的对象锁`。这样`临界区`里所有的就代码可以看做一个原子操作。
比如： A、B两个线程都使用 Object.class 对象来做对象锁。那么B线程无法读到 A线程的中间状态。
如果使用的是不同的对象锁或者有一个线程不使用synchronized，那么就不存在原子性！

###synchronized实现有序性
有序性包括两个方面  “指令重排序” 和 “工作内存与主内存同步延迟” 现象，synchronized实现的只是禁止“工作内存与主内存同步延迟” ，并不会禁止指令重排序。在java中只有volatile关键字才能禁止指令重排序


######为什么synchronized不能禁止指令重排序又能保证有序性？

synchronized不能防止指令重排序，但是能保证有序性，这和volatile实现有序性的方式不同
- synchronized是通过`互斥锁`来保证有序性的，同步块里是单线程的。按照`as-if-serial`语义：即在单线程下不管怎么重排序，程序的执行结果不能被改变。
- 而volatile是通过`内存屏障`实现的有序性，即防止指令重排序来保证有序性。


~~~
注意： synchronized 无法禁止内部区域代码的`指令的重排序优化！

总而言之就是， synchronized 块里的非原子操作依旧可能发生指令重排
~~~

关于as-if-serial语义可以看看我这篇文章
https://www.jianshu.com/p/40cb45484f1e
