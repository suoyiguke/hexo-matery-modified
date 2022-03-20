---
title: java-线程基础之Thread-isAlive()方法.md
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
title: java-线程基础之Thread-isAlive()方法.md
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
看到了一个关于thread.isAlive()方法的选项；
答案表示thread.isAlive()返回 true不只是说明线程在执行中；
于是动手写了个测试用例

![image.png](https://upload-images.jianshu.io/upload_images/13965490-72caf405b5613097.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###java代码
~~~

    public static void main(String[] args) throws InterruptedException {

        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        System.out.println(thread.getState().name() + " "+thread.isAlive());
        thread.start();
        while (true){
            System.out.println(thread.getState().name() + " "+thread.isAlive());
        }
//        thread.join();
//        System.out.println(thread.getState().name() + " "+ thread.isAlive());

    }


~~~

###输出
~~~
NEW false
RUNNABLE true
RUNNABLE true
TIMED_WAITING true
TIMED_WAITING true
RUNNABLE true
RUNNABLE true
RUNNABLE true
TERMINATED false
TERMINATED false
~~~

- new状态 返回false
- runnable 返回true
- timed_waitting 返回true
- terminated 返回false

因此在线程因为sleep进入waitting状态时，isAlive()返回true
那么，线程进入blocked状态呢？

###java代码
~~~
package 多线程编程;

public class Test {


    public static void main(String[] args) throws InterruptedException {


        Thread thread1 = new Thread(new Runnable() {
            @Override
            public void run() {
                synchronized (this){
                    try {
                        System.out.println("优先获得锁的线程");
                        Thread.currentThread().sleep(1000*5);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }
            }
        });

        Thread thread2 = new Thread(new Runnable() {
            @Override
            public void run() {
                synchronized (this){
                    System.out.println("blockd线程");

                }
            }
        });

        thread1.start();
        thread2.start();


        while (true) {
            System.out.println(thread2.getState().name() + " " + thread2.isAlive());
        }

    }

}

~~~
###执行结果
~~~
优先获得锁的线程
RUNNABLE true
blockd线程
BLOCKED true
TERMINATED false
TERMINATED false
TERMINATED false
TERMINATED false
~~~
- 因为锁竞争失败进入blocked状态的线程的isAlive()也返回 true
