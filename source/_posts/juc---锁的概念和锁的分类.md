---
title: juc---锁的概念和锁的分类.md
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
title: juc---锁的概念和锁的分类.md
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
转载至：https://my.oschina.net/ConstXiong/blog/3118284

###锁的概念
在并发编程中，经常会遇到多个线程访问同一个共享变量，当同时对共享变量进行读写操作时，就会产生数据不一致的情况。


为了解决这个问题

JDK 1.5 之前，使用 synchronized 关键字，拿到 Java 对象的锁，保护锁定的代码块。JVM 保证同一时刻只有一个线程可以拿到这个 Java 对象的锁，执行对应的代码块。
JDK 1.5 开始，引入了并发工具包 java.util.concurrent.locks.Lock，让锁的功能更加丰富。

###Java 中常见的锁有
1、synchronized
2、可重入锁 java.util.concurrent.lock.ReentrantLock
3、可重入读写锁 java.util.concurrent.lock.ReentrantReadWriteLock



###锁的使用注意事项
- synchronized 修饰代码块时，最好不要锁定基本类型的包装类，如 jvm 会缓存 -128 ~ 127 Integer 对象，每次向如下方式定义 Integer 对象，会获得同一个 Integer，如果不同地方锁定，可能会导致诡异的性能问题或者死锁
Integer i = 100; 
- synchronized 修饰代码块时，要线程互斥地执行代码块，需要确保锁定的是同一个对象，这点往往在实际编程中会被忽视
- synchronized  不支持尝试获取锁、锁超时和公平锁
- ReentrantLock 一定要记得在 finally{} 语句块中调用 unlock() 方法释放锁，不然可能导致死锁
- ReentrantLock 在并发量很高的情况，由于自旋很消耗 CPU 资源
ReentrantReadWriteLock 适合对共享资源写操作很少，读操作频繁的场景；可以从写锁降级到读锁，无法从读锁升级到写锁



###Java 中不同维度的锁分类
######可重入锁

指在同一个线程在外层方法获取锁的时候，进入内层方法会自动获取锁。JDK 中基本都是可重入锁，避免死锁的发生。上面提到的常见的锁都是可重入锁。
 

######公平锁 / 非公平锁

- 公平锁，指多个线程按照申请锁的顺序来获取锁。如 java.util.concurrent.lock.ReentrantLock.FairSync
- 非公平锁，指多个线程获取锁的顺序并不是按照申请锁的顺序，有可能后申请的线程先获得锁。如 synchronized、java.util.concurrent.lock.ReentrantLock.NonfairSync
        
######独享锁 / 共享锁

- 独享锁，指锁一次只能被一个线程所持有。synchronized、java.util.concurrent.locks.ReentrantLock 都是独享锁
- 共享锁，指锁可被多个线程所持有。ReadWriteLock 返回的 ReadLock 就是共享锁
          
######悲观锁 / 乐观锁

- 悲观锁，一律会对代码块进行加锁，如 synchronized、java.util.concurrent.locks.ReentrantLock
- 乐观锁，默认不会进行并发修改，通常采用 CAS 算法不断尝试更新
悲观锁适合写操作较多的场景，乐观锁适合读操作较多的场景
        
######粗粒度锁 / 细粒度锁

- 粗粒度锁，就是把执行的代码块都锁定
- 细粒度锁，就是锁住尽可能小的代码块，jdk1.7中java.util.concurrent.ConcurrentHashMap 中的分段锁就是一种细粒度锁
- 粗粒度锁和细粒度锁是相对的，没有什么标准
        
######偏向锁 / 轻量级锁 / 重量级锁

- JDK 1.5 之后新增锁的升级机制，提升性能。
通过 synchronized 加锁后，一段同步代码一直被同一个线程所访问，那么该线程获取的就是偏向锁
- 偏向锁被一个其他线程访问时，Java 对象的偏向锁就会升级为轻量级锁
再有其他线程会以自旋的形式尝试获取锁，不会阻塞，自旋一定次数仍然未获取到锁，就会膨胀为重量级锁        
        
######自旋锁

自旋锁是指尝试获取锁的线程不会立即阻塞，而是采用循环的方式去尝试获取锁，这样的好处是减少线程上下文切换的消耗，缺点是循环占有、浪费 CPU 资源.
CAS算法就是一种自旋锁
