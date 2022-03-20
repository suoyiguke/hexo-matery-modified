---
title: juc-引发死锁的场景.md
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
title: juc-引发死锁的场景.md
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
>学而不思则罔，思而不学则殆

死锁：多个线程之间互相持有对方需要的锁导致的持续阻塞问题

######synchronized 嵌套使用不当导致死锁


如下面的程序，线程1 加锁顺序是 a,b ； 线程2 加锁顺序是b,a；
使用CountDownLatch 让线程1先持有a对象锁后等待、让线程2先持有b对象锁后等待；等到main线程执行  countDownLatch.countDown(); 此时线程1和线程2并行执行；那么

>1线程持有a对象锁但是还去竞争b对象锁；
2线程持有b对象锁但是还去竞争a对象锁；

终于互不相让产生死锁

所以在使用synchronized 嵌套时有结论：
>对多个资源、数据库表、对象同时加锁时，需要保持一致的加锁顺序，否则可能会造成死锁。
说明：线程一需要对表 A、 B、 C 依次全部加锁后才可以进行更新操作，那么线程二的加锁顺序也必须是A、 B、 C，否则可能出现死锁。

~~~
package io.renren;
import lombok.SneakyThrows;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

class Account {

    private String name;

    public Account(String name) {
        this.name = name;
    }

    @SneakyThrows
    public static void main(String[] args) {
        CountDownLatch countDownLatch = new CountDownLatch(1);
        Account a = new Account("A");
        Account b = new Account("B");


        new Thread(new Runnable() {
            @Override
            public void run() {
                synchronized (a) {

                    try {
                        countDownLatch.await();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                    synchronized (b) {
                        System.out.println("执行业务.......");

                    }
                }

            }
        }, "1").start();


        new Thread(new Runnable() {
            @Override
            public void run() {

                synchronized (b) {
                    try {
                        countDownLatch.await();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                    synchronized (a) {
                        System.out.println("执行业务.......");
                    }
                }

            }
        }, "2").start();

        TimeUnit.SECONDS.sleep(3);
        countDownLatch.countDown();
    }

}

~~~

执行上面的程序，发现程序迟迟不退出。使用jstack 20784命令查看线程堆栈快照信息，如下

![image.png](https://upload-images.jianshu.io/upload_images/13965490-f0a97286497d228e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

提示找到一个死锁，并且打印了线程1和线程2的持锁等待锁的情况

>- 线程1持有  locked <0x00000000d620f2f8> (a io.renren.Account)，等待 <0x00000000d620f338> (a io.renren.Account)
>- 线程2持有<0x00000000d620f338> (a io.renren.Account)，等待<0x00000000d620f2f8> (a io.renren.Account)
