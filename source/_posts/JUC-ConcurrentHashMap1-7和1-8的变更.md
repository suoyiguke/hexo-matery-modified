---
title: JUC-ConcurrentHashMap1-7和1-8的变更.md
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
title: JUC-ConcurrentHashMap1-7和1-8的变更.md
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
HashMap 是线程不安全的，效率高；HashTable 是线程安全的，效率低。

ConcurrentHashMap 可以做到既是线程安全的，同时也可以有很高的效率，得益于使用了分段锁。

 

###实现原理
###JDK 1.7：

1、ConcurrentHashMap 是通过数组 + 链表实现，由 Segment 数组和 Segment 元素里对应多个 HashEntry 组成value 和链表都是 volatile 修饰，保证可见性

2、ConcurrentHashMap 采用了分段锁技术，分段指的就是 Segment 数组，其中 Segment 继承于 ReentrantLock
理论上 ConcurrentHashMap 支持 CurrencyLevel (Segment 数组数量)的线程并发，每当一个线程占用锁访问一个 Segment 时，不会影响到其他的 Segment
 

######put 方法的逻辑较复杂：

尝试加锁，加锁失败 scanAndLockForPut 方法自旋，超过 MAX_SCAN_RETRIES 次数，改为阻塞锁获取将当前 Segment 中的 table 通过 key 的 hashcode 定位到 HashEntry遍历该 HashEntry，如果不为空则判断传入的 key 和当前遍历的 key 是否相等，相等则覆盖旧的 value不为空则需要新建一个 HashEntry 并加入到 Segment 中，同时会先判断是否需要扩容最后释放所获取当前 Segment 的锁
 

######get 方法较简单：

将 key 通过 hash 之后定位到具体的 Segment，再通过一次 hash 定位到具体的元素上由于 HashEntry 中的 value 属性是用 volatile 关键词修饰的，保证了其内存可见性
 

###JDK 1.8：

1、抛弃了原有的 Segment 分段锁，采用了 CAS + synchronized 来保证并发安全性

2、HashEntry 改为 Node，作用相同。val next 都用了 volatile 修饰
 

######put 方法逻辑：

根据 key 计算出 hash 值判断是否需要进行初始化
根据 key 定位出的 Node，如果为空表示当前位置可以写入数据，利用 CAS 尝试写入，失败则自旋如果当前位置的 hashcode == MOVED == -1，则需要扩容如果都不满足，则利用 synchronized 锁写入数据如果数量大于 TREEIFY_THRESHOLD 则转换为红黑树
 

######get 方法逻辑：

根据计算出来的 hash 值寻址，如果在桶上直接返回值如果是红黑树，按照树的方式获取值如果是链表，按链表的方式遍历获取值
 

###JDK 1.7 到 JDK 1.8 中的 ConcurrentHashMap 最大的改动：

链表上的 Node 超过 8 个改为红黑树，查询复杂度 O(logn)
ReentrantLock 显示锁改为 synchronized，说明 JDK 1.8 中 synchronized 锁性能赶上或超过 ReentrantLock
