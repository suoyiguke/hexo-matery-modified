---
title: juc---Lock接口之tryLock尝试加锁（三）.md
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
title: juc---Lock接口之tryLock尝试加锁（三）.md
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
>我辈岂是蓬蒿人 

tryLock()会去尝试获取锁，如果锁是被占有的状态，那么它会马上返回false。不会像 lock.lock()方法那样一直阻塞下去。这就是它的特点与优势。
而且tryLock()有两个重载方法如下

>boolean tryLock();
boolean tryLock(long time, TimeUnit unit) throws InterruptedException;

另一个tryLock方法可以传入时间参数，指定超时时间。在指定时间内若仍未获取到锁则一直阻塞下去，阻塞时间超过指定时间后就会返回false

现在我们分别来使用这两个方法

######lock.tryLock()
>这个无参数的tryLock不会引发锁等待阻塞；如果锁可用，则获取锁，并立即返回值 true；如果锁不可用，则此方法将立即返回值 false


~~~
package io.renren;
import org.elasticsearch.indices.flush.ShardsSyncedFlushResult;

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

        if(lock.tryLock()){
            try{
                System.out.println(Thread.currentThread().getName()+"获取到锁！");
            }finally {
                // 不执行 lock.unlock(); lock将一直被A线程占用，即是A线程执行完毕终止，锁也不会释放！！
            }
        }else{
            System.out.println(Thread.currentThread().getName()+"未获取到锁");
        }


    }

    public static void main(String[] args) throws IOException, InterruptedException {

        Thread thread1 = new Thread(new TestLock());
        thread1.setName("A");
        Thread thread2 = new Thread(new TestLock());
        thread2.setName("B");
        thread1.start();


        //让A线程先执行，先获取锁，这样B线程获取不到锁
        TimeUnit.SECONDS.sleep(3);
        thread2.start();


    }

}
~~~
上面的程序A线程优先执行，先获取到了锁。并且不进行unlock解锁操作。那么A线程将一直持久锁，即是A线程终止也不会释放锁。那么B线程将无法获取到锁，tryLock立马返回false。
执行程序，控制台打印如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ace03ec4ba561c2a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######boolean tryLock(long time, TimeUnit unit) throws InterruptedException;

>这个tryLock重载 指定了锁等待超时时间，而且响应中断

~~~
package io.renren;
import org.elasticsearch.indices.flush.ShardsSyncedFlushResult;

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
            if(lock.tryLock(5,TimeUnit.SECONDS)){
                try{
                    System.out.println(Thread.currentThread().getName()+"获取到锁！");
                }finally {
                    //等待2秒再执行解锁
                     TimeUnit.SECONDS.sleep(2);
                     lock.unlock();
                }
            }else{
                System.out.println(Thread.currentThread().getName()+"未获取到锁");
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }


    }

    public static void main(String[] args) throws IOException, InterruptedException {

        Thread thread1 = new Thread(new TestLock());
        thread1.setName("A");
        Thread thread2 = new Thread(new TestLock());
        thread2.setName("B");
        thread1.start();


        //让A线程先执行，先获取锁
        TimeUnit.SECONDS.sleep(3);
        thread2.start();


    }

}
~~~

上面的程序中A线程优先执行，先获取到了锁。期间A线程睡眠了2秒再执行unlock解锁操作。B线程在它睡眠期间已经start，因为执行了lock.tryLock(5,TimeUnit.SECONDS) 会引发至少5秒的锁等待，等到A线程终于睡眠完毕执行了unlock操作后，B线程便获取到了锁

控制台打印如下

![image.png](https://upload-images.jianshu.io/upload_images/13965490-72e5b683fa027ce4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######tryLock阻塞的线程状态和是否会响应线程中断
我们知道有参数的tryLock重载方法，它有抛出InterruptedException异常。说明它是响应中断的
>boolean tryLock(long time, TimeUnit unit) throws InterruptedException;

~~~
package io.renren;
import org.elasticsearch.indices.flush.ShardsSyncedFlushResult;

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
            if(lock.tryLock(10,TimeUnit.SECONDS)){
                try{
                    System.out.println(Thread.currentThread().getName()+"获取到锁！");
                }finally {
                }
            }else{
                System.out.println(Thread.currentThread().getName()+"未获取到锁");
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }


    }

    public static void main(String[] args) throws IOException, InterruptedException {

        Thread thread1 = new Thread(new TestLock());
        thread1.setName("A");
        Thread thread2 = new Thread(new TestLock());
        thread2.setName("B");
        thread1.start();


        //让A线程先执行，先获取锁
        TimeUnit.SECONDS.sleep(3);
        thread2.start();


        TimeUnit.SECONDS.sleep(1);
        System.out.println(thread2.getState());

        //中断thread2
        thread2.interrupt();
        TimeUnit.SECONDS.sleep(1);
        //打印中断标志位为 false 
        System.out.println(thread2.isInterrupted());

    }

}
~~~

执行上面的程序，控制台打印情况如下

![image.png](https://upload-images.jianshu.io/upload_images/13965490-8d40a129b1632f0d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

有时间参数的tryLock引发的阻塞对应的线程状态是`TIMED_WAITING` 该阻塞可以响应线程中断！


######如何正确的使用lock.tryLock()方法


首先是错误示范：
若当前线程并未获得锁而调用了 lock.unlock(); java.lang.IllegalMonitorStateException 则会抛出异常，如下示例

~~~
package io.renren;

import lombok.SneakyThrows;
import org.elasticsearch.indices.flush.ShardsSyncedFlushResult;

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

        lock.tryLock();//tryLock有可能不会获得锁
        try {
            System.out.println(Thread.currentThread().getName()+"执行业务.....");
        }finally {
            TimeUnit.SECONDS.sleep(3);
            lock.unlock();//当前线程没有持有锁的情况下，执行unlock
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


    }

}
~~~
执行结果如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3b4f08e981e9e050.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


正确使用：在使用尝试机制来获取锁的方式中，进入业务代码块之前，必须先判断当前线程是否持有锁。正确使用方式如下
~~~

         if(lock.tryLock()){
            try{
                System.out.println("执行业务.....");
            }finally {
                lock.unlock();
            }
        }

~~~
