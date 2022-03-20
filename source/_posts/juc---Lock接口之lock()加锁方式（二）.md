---
title: juc---Lock接口之lock()加锁方式（二）.md
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
title: juc---Lock接口之lock()加锁方式（二）.md
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
> 理解万岁

######如何正确的使用lock.lock()方法
在使用阻塞等待获取锁的方式中，必须在try代码块之外，并且在加锁方法与try代码块之间没有任何可能抛出异常的方法调用，避免加锁成功后，在finally中无法解锁。

1、如果在lock方法与try代码块之间的方法调用抛出异常，那么无法解锁，造成其它线程无法成功获取锁。

我们可以举例如下：
~~~
package io.renren;
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

    @Override
    public void run() {
        try {
            TimeUnit.SECONDS.sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        lock.lock();
        int a = 1 / 0;//出现异常，无法解锁
        try {

        } finally {
            lock.unlock();
        }
    }

    public static void main(String[] args) throws IOException, InterruptedException {

        Thread thread1 = new Thread(new TestLock());
        thread1.setName("A");
        Thread thread2 = new Thread(new TestLock());
        thread2.setName("B");
        thread1.start();


        TimeUnit.SECONDS.sleep(3);
        thread2.start();

        thread1.join();
        thread2.join();


    }

}
~~~
运行程序可以发现A线程因为先执行先获得锁，在进入try语句块之前加锁，中间出现了除0异常。导致无法执行finally 语句块中的`lock.unlock();`解锁操作。这样B线程执行到`lock.lock();`时迟迟无法获得锁。`最终B线程永久阻塞下去`




2、如果lock方法在try代码块之内，可能由于其它方法抛出异常，导致在finally代码块中，unlock对未加锁的对象解锁，它会调用AQS的tryRelease方法（取决于具体实现类），抛出IllegalMonitorStateException异常。
我们可以看看下面的例子
~~~
package io.renren;
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

    @Override
    public void run() {
        try {
            TimeUnit.SECONDS.sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        try {
            int a = 1/0;
            lock.lock();//lock不会被执行
        } finally {
            lock.unlock();
        }
    }

    public static void main(String[] args) throws IOException, InterruptedException {
        new Thread(new TestLock()).start();
    }

}
~~~
这段程序因为在执行lock.lock();加锁之前就出现了异常，那么lock.lock();不会得到执行，但是finally 中的lock.unlock();却会执行
所以报出 java.lang.IllegalMonitorStateException异常

因此` lock.lock(); ` 不允许放到try代码块之内

3、 在Lock对象的lock方法实现中可能抛出unchecked异常，产生的后果与说明二相同。 java.concurrent.LockShouldWithTryFinallyRule.rule.desc
            

###总结
 所以这规范要求 ` lock.lock(); `必须紧跟try代码块，且unlock要放到finally第一行。最终的写法需要按照如下例子
~~~
    Lock lock = new XxxLock();
    // ...
    lock.lock(); //最靠近try 
    try {
        doSomething();
        doOthers();
    } finally {
        lock.unlock(); // finally 的第一行
    }
~~~

######Lock.lock()的引发阻塞时的线程状态和是否可中断实验

~~~
package io.renren;
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

    @Override
    public void run() {

        lock.lock();

    }

    public static void main(String[] args) throws IOException, InterruptedException {

        Thread thread1 = new Thread(new TestLock());
        thread1.setName("A");
        Thread thread2 = new Thread(new TestLock());
        thread2.setName("B");
        thread1.start();


        //让A线程先执行，先获取锁，这样B线程会一直阻塞下去
        TimeUnit.SECONDS.sleep(3);
        thread2.start();

        TimeUnit.SECONDS.sleep(1);
        System.out.println(thread2.getState()); //WAITING


    }

}
~~~

运行上面程序，控制台打印WAITING。可知lock.lock()方法引发的阻塞时线程状态是WAITING

按理说lock()接口的源码并没有抛出InterruptedException异常，那么它是不会响应中断信号的。但是我也想做下实验看看如何
在上面程序的尾巴上加上这个代码，重新运行。可以得出lock.lock()方法的确不会响应中断信号，仅仅把中断标志设为了true
~~~
      //中断thread2
        thread2.interrupt();

        //打印中断标志位为 true
        System.out.println(thread2.isInterrupted());

~~~

