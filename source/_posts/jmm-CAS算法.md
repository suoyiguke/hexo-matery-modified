---
title: jmm-CAS算法.md
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
title: jmm-CAS算法.md
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
>君子不器

###什么是CAS?
CAS 是 Compare and Swap `比较与交换` 的英文开头字母缩写 

CAS操作（又称为无锁操作）是一种`乐观锁策略`。之前在mysql中使用数据版本号来解决更新丢失的事务并发问题就是使用这中乐观锁机制。 可以回顾一下 https://www.jianshu.com/p/bfd7c684412d

它假设所有线程访问共享资源的时候不会出现冲突（乐观思想）。既然不会冲突那么就不会阻塞线程执行。CAS采用一种：*出现冲突就重试直到当前操作没有冲突为止* 的策略

###CAS的操作过程

CAS比较交换的过程可以通俗的理解为CAS(V,O,N)，它包含三个操作数 
>- V 内存地址存放的实际值；
>- O 预期的值（旧值）；
>- N 更新的新值。

当 V和O相同时，也就是说旧值和内存中实际的值相同表明该值没有被其他线程更改过，即该旧值O就是目前来说最新的值了，自然而然可以将新值N赋值给V。
若 V和O不相同，表明该值已经被其他线程改过了则该旧值O不是最新版本的值了，所以不能将新值N赋给V，返回V即可。
当多个线程使用CAS操作一个变量时只有一个线程会成功，并成功更新，其余会失败。失败的线程会一直重新尝试，`直到更新成功为止`。



###java中CAS的应用

CAS的实现需要硬件指令集的支撑，在JDK1.5后虚拟机才可以使用处理器提供的CMPXCHG指令实现。

java.util.concurrent.atomic包下的原子操作类大量使用CAS算法。可以看看其中的AtomicInteger类的源码：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3eac183bca1163c0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

明显，调用了Unsafe类的getAndAddInt方法。那么再跟进去看看
![image.png](https://upload-images.jianshu.io/upload_images/13965490-70445e2756cea56a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
此时已经很清晰了，它又调用了一个名为compareAndSwapInt的方法

我们可以看看sun.misc.Unsafe类，这三个方法均是去调用CAS算法。不过都是native的，说明比较底层了，借助C来调用CPU底层指令实现的。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7ad128b4ea7b9dd5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




###CAS带来的问题

######ABA问题
因为CAS会检查旧值有没有变化。比如一个旧值A变为了成B，然后再变成A，刚好在做CAS时检查发现旧值并没有变化依然为A，但是实际上的确发生了变化。

就像日常生活中，A同学把盒子放到地上，然后B同学把盒子拿开，之后C同学又把盒子放到了地上。那么这个情景下最终的结果是盒子一直没有离开过地面。显然这个结论是不正确的。

解决方案可以沿袭数据库中常用的乐观锁方式，添加一个版本号可以解决。原来的变化路径A->B->A就变成了1A->2B->3C。

######自旋时间过长

使用CAS是非阻塞同步，并不会将线程挂起，其实是`自旋` ，即再进行下一次尝试，如果这里自旋时间过长对性能是很大的消耗。因为`自旋操作`是占有cup执行时间片的。如果JVM能支持处理器提供的pause指令，那么在效率上会有一定的提升。

所以在激烈的并发修改情景下，是不推荐使用CAS/乐观锁机制的。
>但是在jdk1.8中 新增了LongAdder 类可以用来代替原来的AtomicLong，在高并发修改下LongAdder 性能强过AtomicLong。同样LongAdder 也是采用CAS算法保证原子性，但是它还使用了一种`分散热点`的思想进行了优化。



######只能保证一个变量的原子性

当对一个共享变量执行操作时，我们可以使用循环CAS的方式来保证原子操作，但是对多个共享变量操作时，循环CAS就无法保证操作的原子性，这个时候就可以用锁保证原子性。

>或者把多个共享变量合并成一个共享变量来操作。比如有两个共享变量i＝1,j=2，合并一下ij=12，然后用CAS来操作ij。JDK其实提供了AtomicReference类来保证引用对象之间的原子性，我们可以把多个变量放在一个对象里来进行CAS操作。
