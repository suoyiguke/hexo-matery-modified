---
title: juc---Lock接口之lockInterruptibly可中断阻塞的加锁方法（四）.md
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
title: juc---Lock接口之lockInterruptibly可中断阻塞的加锁方法（四）.md
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
> 人生如逆旅，我亦是行人


Lock接口还提供了一个lockInterruptibly()方法，从名字来看他就和线程中断有着紧密的联系。。
Lock接口的lockInterruptibly方法 源码如下
> void lockInterruptibly() throws InterruptedException;

明显lockInterruptibly方法后面抛出了InterruptedException异常，这既是意味着该方法引发的阻塞时可以中断的 ~

其实就可以理解为lockInterruptibly()方法是lock()方法的可中断版本；当然上面文章也提到了 boolean tryLock(long time, TimeUnit unit) 方法引发的锁等待阻塞也可中断


可以看看下面的程序例子
~~~
package io.renren;
import lombok.SneakyThrows;

import java.io.IOException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * @description: TestLock
 * @author: yinkai
 * @create: 2020/3/15 21:52
 */
public class TestLock implements Runnable {
    static Lock lock = new ReentrantLock();

    @SneakyThrows
    @Override
    public void run() {

        lock.lockInterruptibly();
        try {
            System.out.println(Thread.currentThread().getName()+"执行业务.....");
        }finally {
            TimeUnit.SECONDS.sleep(5);
            lock.unlock();
        }

    }

    public static void main(String[] args) throws IOException, InterruptedException {

        Thread thread1 = new Thread(new TestLock());
        thread1.setName("A");
        Thread thread2 = new Thread(new TestLock());
        thread2.setName("B");
        thread1.start();


        //让A线程先执行，先获取锁
        TimeUnit.SECONDS.sleep(1);
        thread2.start();

        //中断线程
        thread2.interrupt();
        TimeUnit.SECONDS.sleep(1);
        //抛出了中断异常，打印false
        System.out.println(thread2.isInterrupted());


    }

}
~~~

A线程优先执行，先获得锁，并在sleep 5秒之后才解锁。那么在A线程解锁之前B线程也开始执行，在此期间B线程无法获得锁一直处于阻塞状态。当main线程执行thread2.interrupt(); 时B线程抛出java.lang.InterruptedException异常，并且 System.out.println(thread2.isInterrupted());打印false

这个程序足矣证明lockInterruptibly方法引发的等待锁阻塞可以被中断！

lockInterruptibly引发的等待锁阻塞如果迟迟没有获得锁，且没有调用阻塞线程的中断方法。那么此线程将一直阻塞下去
