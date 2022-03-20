---
title: juc----ReentrantLock和Condition的await-signal机制.md
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
title: juc----ReentrantLock和Condition的await-signal机制.md
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



- await-signal的出现是为了代替wait-notify，比它更加强大
- 我的这篇文章有对wait-notify进行介绍
https://www.jianshu.com/p/36b57330531c

**await-signal与wait-notify进行对比**
synchronized  ====> lock 
Object=====> Condition
Object.wait() ======> Condition.await()
Object.notify() ======>Condition.signal()

######lock接口的方法介绍
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8641ee9a929e2719.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######Condition类的方法介绍
![image.png](https://upload-images.jianshu.io/upload_images/13965490-8383935afbaea1c7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######lock的await-signal机制使用示例
这个例子说明了await-signal可以代替wait-notify
~~~
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

class MpCust {

    private ReentrantLock lock = new ReentrantLock();
    private Condition condition = lock.newCondition();
    private int number = 0;
    public  void increment() throws InterruptedException {
        try {
            lock.lock();

            while (number != 0){
                condition.await();
            }
            number++;
            System.out.println(Thread.currentThread().getName()+"\n"+number);
            condition.signalAll();

        }finally {
            lock.unlock();
        }


    }

    public  void decrement() throws InterruptedException {
        try {
            lock.lock();
            while (number==0){
                condition.await();
            }
            number--;
            System.out.println(Thread.currentThread().getName()+"\n"+number);
            condition.signalAll();
        }finally {
            lock.unlock();
        }

    }

    public static void main(String[] args) {
        MpCust mpCust = new MpCust();

        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(300);
                        mpCust.increment();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"A").start();


        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(400);
                        mpCust.decrement();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"B").start();




        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(300);
                        mpCust.increment();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"C").start();


        new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    try {
                        Thread.sleep(400);
                        mpCust.decrement();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }

            }
        },"D").start();


    }

}
~~~

######await-signal能实现`精确的唤醒`
需求：
3个线程启动
A线程打印3次，然后B线程打印5次，然后C线程打印10次
A线程打印3次，然后B线程打印5次，然后C线程打印10次
.....
重复10次



**实现如下：**
需要一个标志位flag来实现这个功能！

分四步走：
①、while判断flag标志位进行wait()
②、编写线程业务逻辑
③、修改flag标志位
④、在指定的Condition上通知 signal()
~~~
 static int flag = 1;
~~~

~~~
package org.jeecg;

import javax.swing.plaf.synth.SynthScrollBarUI;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantLock;

/**
 *@program: jeecg-boot-parent
 *@description:
 *@author: yinkai
 *@create: 2020-04-29 10:16
 */
public class Main {


    static ReentrantLock  lock = new ReentrantLock();
    static Condition condition1 =  lock.newCondition();
    static Condition condition2 =  lock.newCondition();
    static Condition condition3 =  lock.newCondition();
    static volatile int flag = 1;


    public static void main(String[] args) {



        new Thread(new Runnable() {
            @Override
            public void run() {

                for (int j = 0; j < 10 ; j++) {
                    lock.lock();
                    try {
                        while (flag != 1){
                            try {
                                condition1.await();
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                        }

                        for (int i = 0; i < 3; i++) {
                            System.out.println("A");
                        }
                        flag = 2;
                        condition2.signalAll();

                    }finally {
                        lock.unlock();

                    }
                }


            }
        },"A").start();




        new Thread(new Runnable() {
            @Override
            public void run() {

                for (int j = 0; j < 10; j++) {
                    lock.lock();
                    try {
                        while (flag != 2){
                            try {
                                condition2.await();
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                        }
                        for (int i = 0; i < 5; i++) {
                            System.out.println("B");
                        }

                        flag = 3;
                        condition3.signalAll();
                    }finally {
                        lock.unlock();
                    }
                }

            }
        },"B").start();



        new Thread(new Runnable() {
            @Override
            public void run() {

                for (int j = 0; j < 10; j++) {
                    lock.lock();
                    try {
                        while (flag != 3){
                            try {
                                condition3.await();
                            } catch (InterruptedException e) {
                                e.printStackTrace();
                            }
                        }
                        for (int i = 0; i < 10; i++) {
                            System.out.println("C");
                        }
                        flag = 1;
                        condition1.signalAll();
                    }finally {

                        lock.unlock();
                    }
                }

            }
        },"C").start();


    }

}
~~~


######简化版，三个线程依次输出aaa，bbbb，ccccc
~~~
package com.company;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * @program: String
 * @description:
 * @author: yinkai
 * @create: 2020-03-25 11:32
 */
public class Test {

    static ReentrantLock lock = new ReentrantLock();
    static Condition condition1 = lock.newCondition();
    static Condition condition2 = lock.newCondition();
    static Condition condition3 = lock.newCondition();
    volatile static int flag = 0;


    public static void main(String[] args) {

        Thread threadA = new Thread(new Runnable() {
            @Override
            public void run() {

                lock.lock();
                try {
                    while (flag != 1) {
                        condition1.await();
                    }

                    for (int i = 0; i < 3; i++) {
                        System.out.println("A");
                    }
                    flag = 2;
                    condition2.signalAll();

                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    lock.unlock();
                }


            }
        }, "A");


        Thread threadB = new Thread(new Runnable() {
            @Override
            public void run() {

                lock.lock();
                try {
                    while (flag != 2) {
                        condition2.await();
                    }

                    for (int i = 0; i < 4; i++) {
                        System.out.println("B");
                    }

                    flag = 3;
                    condition3.signalAll();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    lock.unlock();
                }


            }
        }, "B");


        Thread threadC = new Thread(new Runnable() {
            @Override
            public void run() {

                lock.lock();
                try {
                    while (flag != 3) {
                        condition3.await();
                    }

                    for (int i = 0; i < 5; i++) {
                        System.out.println("C");
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    lock.unlock();
                }


            }
        }, "C");


        threadA.start();
        threadB.start();
        threadC.start();
        flag = 1;


    }


}
~~~

###使用注意
await-signal方法请放到到 lock 和unlock语句块之间！
