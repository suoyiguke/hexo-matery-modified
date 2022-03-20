---
title: juc---Lock接口的基本概念（一）.md
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
title: juc---Lock接口的基本概念（一）.md
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
> 今人不见古时月，今月曾经照古人

我们可以使用 java.util.concurrent.locks.Lock 来代替synchronized同步块。它的功能更加强大；
######Lock相对于synchronized有以下优点

- Lock 可以尝试获取锁 ，如果无法获取，并不会阻塞下去而是立即返回。（尝试获取锁/无阻塞获取锁）
- Lock 获取锁引发的阻塞可设置超时时间 （可超时）
- Lock 获取锁引发的阻塞可以被中断 （可中断）
- Lock 支持多个相关联的对象Condition (可以实现精确的唤醒) （synchronized只能随机的唤醒一个线程[notify]或者直接唤醒全部线程[notifyAll]）
- Lock 的实现类如ReentrantLock  可以实现`公平锁`，即先等待先获取到锁
- Lock的实现类如 ReadWriteLock 的读锁可以实现 `并发读` 
  关于ReadWriteLock 可以看看这篇文章https://www.jianshu.com/p/c2180c2ca8b7



######有优点就会有缺陷 
Lock需要程序员显式的加锁和解锁。如果lock使用不当，很可能引发死锁或者出现为占有锁而解锁的异常；所以如何正确的使用Lock是一个非常讲究的问题

那么应该如何正确科学的使用Lock呢？可以看看我的这篇文章
https://www.jianshu.com/p/418a9217fe51
 
######Lock接口是实现类有： 

ReentrantLock ， ReentrantReadWriteLock.ReadLock ， ReentrantReadWriteLock.WriteLock 







######Lock具备synchronized一样的内存语义
  所有`Lock`实施必须执行与内置监视器锁相同的内存同步语义，如The Java Language Specification (17.4 Memory Model) 所述

>- 成功的`lock`操作具有与成功锁定动作相同的内存同步效果。
>-  成功的`unlock`操作具有与成功解锁动作相同的内存同步效果。
>-  不成功的锁定和解锁操作以及重入锁定/解锁操作，不需要任何内存同步效果。

所谓的`内存同步效果` 即是：
>1、线程解锁前，必须把工作内存中共享变量的最新值刷新到主内存中
2、线程加锁时，将清空工作内存中共享变量的值，从而使用共享变量时需要从主内存中重新获取最新的值（注意：加锁与解锁需要是同一把锁）



######我们来看看这个Lock接口，它有6个方法
![image.png](https://upload-images.jianshu.io/upload_images/13965490-5259e0fb24322fad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 其中有4个加锁方法：
>void lock();
void lockInterruptibly() throws InterruptedException;
boolean tryLock();
    boolean tryLock(long time, TimeUnit unit) throws InterruptedException;

- 1个解锁方法
>void unlock();
- 1个得到Condition的方法
>Condition newCondition();

######关于Lock接口的4个加锁方法皆有不同
假如线程A和线程B使用同一个锁lock，此时线程A首先获取到锁lock.lock()，并且始终持有不释放。如果此时B要去获取锁，有四种方式：  

- lock.lock(): 此方式会始终处于等待中，即使调用B.interrupt()也不能中断，除非线程A调用LOCK.unlock()释放锁。
  
- lock.lockInterruptibly(): 此方式会等待，但当调用B.interrupt()会被中断等待，并抛出InterruptedException异常，否则会与lock()一样始终处于等待中，直到线程A释放锁。 lockInterruptibly的使用看这里 https://www.jianshu.com/p/8f5c273507b2

- lock.tryLock(): 该处不会等待，获取不到锁并直接返回false，去执行下面的逻辑。  

- lock.tryLock(10, TimeUnit.SECONDS)：该处会在10秒时间内处于等待中，当调用B.interrupt()会被中断等待，并抛出InterruptedException。10秒时间内如果线程A释放锁，会获取到锁并返回true，否则10秒过后会获取不到锁并返回false，去执行下面的逻辑。tryLock的详细使用请看这里https://www.jianshu.com/p/c42f93a86c65
