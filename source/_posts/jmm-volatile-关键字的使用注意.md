---
title: jmm-volatile-关键字的使用注意.md
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
title: jmm-volatile-关键字的使用注意.md
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
> 忍耐有多久，器量就有多大

>【参考】 volatile 解决多线程内存不可见问题。对于一写多读，是可以解决变量同步问题，但是如果多写，同样无法解决线程安全问题。
说明：如果是 count++操作，使用如下类实现：AtomicInteger count = new AtomicInteger();count.addAndGet(1); 如果是 JDK8，推荐使用 LongAdder 对象，比 AtomicLong 性能更好（减少乐观锁的重试次数）。


volatile可以解决修饰变量（基本数据类型或者引用性变量，不保证引用型变量指向对象的可见性）的内存可见性，可以保证double和long型变量的get/set操作的原子性，而++操作本身不是原子性的，可能出现线程安全问题，如果要保证多线程操作的正确性，需要使用原子类(Atomic*)或者同步锁

