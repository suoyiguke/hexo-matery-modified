---
title: juc---读写锁ReadWriteLock的使用.md
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
title: juc---读写锁ReadWriteLock的使用.md
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
ReentrantReadWriteLock是ReentrantLock的升级版。它允许读操作并发，性能优于ReentrantLock。
下面通过3个例子，分别比较不加锁、使用ReentrantLock、使用ReentrantReadWriteLock对HashMap的并发读写的影响

######不加锁的程序
~~~
import java.util.HashMap;
import java.util.concurrent.TimeUnit;

public class Test {

    static HashMap<Integer, Integer> hashMap = new HashMap<>();

    static void put(Integer key, Integer value) {

        try {
            System.out.println(Thread.currentThread().getName()+ "  ==开始写入" + value);
            TimeUnit.MILLISECONDS.sleep(300);
            hashMap.put(key, value);
            System.out.println("写入完成");

        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
        }

    }

    static void get(Integer key) {
        try {
            System.out.println(Thread.currentThread().getName() + "  读取数据");
            TimeUnit.MILLISECONDS.sleep(300);
            Integer integer = hashMap.get(key);
            System.out.println("读取完成" + integer);

        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
        }

    }

    public static void main(String[] args) {

        for (int i = 1; i <= 5; i++) {
            int finalI = i;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    Test.put(finalI, finalI);
                }
            }, String.valueOf(i)).start();
        }


        for (int i = 1; i <= 5; i++) {
            int finalI = i;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    Test.get(finalI);
                }
            }, String.valueOf(i)).start();
        }

    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-4638f78123f41674.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

不加锁的程序有明显的线程安全问题：在第一个写操作还没完成的时候，就有第二个写操作过来了；存在`并发写写`、`并发写读`的问题。为了程序的线程安全需要保证`写与写互斥、写与读互斥`


######使用普通的ReentrantLock
~~~
import java.util.HashMap;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Test {

    static HashMap<Integer, Integer> hashMap = new HashMap<>();
    static Lock lock = new ReentrantLock();

    static void put(Integer key, Integer value) {

        lock.lock();
        try {
            System.out.println(Thread.currentThread().getName()+ "  ==开始写入" + value);
            TimeUnit.MILLISECONDS.sleep(300);
            hashMap.put(key, value);
            System.out.println("写入完成");

        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }

    }

    static void get(Integer key) {
        lock.lock();
        try {
            System.out.println(Thread.currentThread().getName() + "  读取数据");
            TimeUnit.MILLISECONDS.sleep(300);
            Integer integer = hashMap.get(key);
            System.out.println("读取完成" + integer);

        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }

    }

    public static void main(String[] args) {

        for (int i = 1; i <= 5; i++) {
            int finalI = i;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    Test.put(finalI, finalI);
                }
            }, String.valueOf(i)).start();
        }


        for (int i = 1; i <= 5; i++) {
            int finalI = i;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    Test.get(finalI);
                }
            }, String.valueOf(i)).start();
        }

    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-66ac97021542932c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

普通的ReadWriteLock虽然禁止了 `并发写写`、`并发写读`、`并发读写`，但是它却将`并发读读` 一杆子打死了。在这种情况`并发读读`是线程安全的，所以这种时候使用ReadWriteLock对效率上的考虑有问题

######使用读写锁ReadWriteLock


~~~
import java.util.HashMap;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class Test {

    static HashMap<Integer, Integer> hashMap = new HashMap<>();
    static ReadWriteLock readWriteLock = new ReentrantReadWriteLock();

    static void put(Integer key, Integer value) {

        readWriteLock.writeLock().lock();
        try {
            System.out.println(Thread.currentThread().getName()+ "  ==开始写入" + value);
            TimeUnit.MILLISECONDS.sleep(300);
            hashMap.put(key, value);
            System.out.println("写入完成");

        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            readWriteLock.writeLock().unlock();
        }

    }

    static void get(Integer key) {
        readWriteLock.readLock().lock();
        try {
            System.out.println(Thread.currentThread().getName() + "  读取数据");
            TimeUnit.MILLISECONDS.sleep(300);
            Integer integer = hashMap.get(key);
            System.out.println("读取完成" + integer);

        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            readWriteLock.readLock().unlock();
        }

    }

    public static void main(String[] args) {

        for (int i = 1; i <= 5; i++) {
            int finalI = i;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    Test.put(finalI, finalI);
                }
            }, String.valueOf(i)).start();
        }


        for (int i = 1; i <= 5; i++) {
            int finalI = i;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    Test.get(finalI);
                }
            }, String.valueOf(i)).start();
        }

    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-acafbd7e6d718981.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


可见ReadWriteLock不允许`并发写写`、`并发写读`、`并发读写`
但允许并发`读读`。这就是ReadWriteLock相对于ReentrantLock的优势！

readWriteLock.readLock() 是一种`共享锁`，它可以被多个线程持有。所以请加读操作上！

