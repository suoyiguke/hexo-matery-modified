---
title: juc-Atomic-之-lazySet.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
---
title: juc-Atomic-之-lazySet.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: juc
categories: juc
---
lazySet是使用Unsafe.putOrderedObject方法，这个方法在对低延迟代码是很有用的，它能够实现非堵塞的写入，这些写入不会被Java的JIT重新排序指令(instruction reordering)，这样它使用快速的存储-存储(store-store) barrier, 而不是较慢的存储-加载(store-load) barrier, 后者总是用在volatile的写操作上，这种性能提升是有代价的，虽然便宜，也就是写后结果并不会被其他线程看到，甚至是自己的线程，通常是几纳秒后被其他线程看到，这个时间比较短，所以代价可以忍受。

类似Unsafe.putOrderedObject还有unsafe.putOrderedLong等方法，unsafe.putOrderedLong比使用 volatile long要快3倍左右。.

在DDD中有值对象概念，值对象的特点是不可变的，而我们经常要修改的状态是可变的，结合lazySet和值对象我们可以编写并发性很好的可变状态修改。

比如：Forum论坛有一个论坛状态ForumState，论坛状态主要是当前最新的帖子等信息，每次有新贴发布时，会更新论坛状态，我们将ForumState设计成一个值对象，一旦有新的帖子发布，就创建一个新的对象 ForumState，然后替换掉旧的状态，这种替换动作可以使用AtomicLong.lazySet来完成。
