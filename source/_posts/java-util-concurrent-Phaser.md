---
title: java-util-concurrent-Phaser.md
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
title: java-util-concurrent-Phaser.md
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
Phaser 比较适合这样一种场景，一种任务可以分为多个阶段，希望多个线程去处理该批任务，对于每个阶段，多个线程可以并发进行，但是希望保证只有前面一个阶段的任务完成之后才能开始后面的任务。

这种场景可以使用多个CyclicBarrier来实现，每个CyclicBarrier负责等待一个阶段的任务全部完成。

但是使用CyclicBarrier的缺点在于，需要明确知道总共有多少个阶段，同时并行的任务数需要提前预定义好，且无法动态修改。而Phaser可同时解决这两个问题。


1、传统用法：发令枪
~~~
package com.company;

import java.util.concurrent.Phaser;
import java.util.concurrent.TimeUnit;

public class Merge2 {


    public static void main(String[] args)  {
        final Phaser phaser = new Phaser(1);

        new Thread(new Runnable() {
            @Override
            public void run() {

                try {
                    phaser.awaitAdvanceInterruptibly(0);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println(Thread.currentThread().getName()+System.currentTimeMillis());
            }
        }).start();


        new Thread(new Runnable() {
            @Override
            public void run() {

                try {
                    phaser.awaitAdvanceInterruptibly(0);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println(Thread.currentThread().getName()+System.currentTimeMillis());
            }
        }).start();



        new Thread(new Runnable() {
            @Override
            public void run() {

                try {
                    phaser.awaitAdvanceInterruptibly(0);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println(Thread.currentThread().getName()+System.currentTimeMillis());
            }
        }).start();


        try {
            TimeUnit.SECONDS.sleep(5);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        //phase加1
        phaser.arriveAndDeregister();
        System.out.println(Thread.currentThread().getName()+System.currentTimeMillis());

    }

}
~~~

2、将一个任务分为3个阶段，每个阶段有3个线程完成。多个线程必须等到其它线程的同一阶段的任务全部完成才能进行到下一个阶段，并且每当完成某一阶段任务时，Phaser都会执行其onAdvance方法。




~~~
package com.company;

import java.util.concurrent.Phaser;

public class Merge2 {
    public static void main(String[] args) {
        int threadNum = 3;
        int phases = 4;
        final Phaser phaser = new Phaser(threadNum) {
            @Override
            protected boolean onAdvance(int phase, int registeredParties) {
                System.out.println("====== Phase : " + phase + " 阶段完成 ======");
                return registeredParties == 0;
            }
        };

        for (int i = 0; i < threadNum; i++) {
            int threadId = i;
            Thread thread = new Thread(() -> {
                for (int phase = 0; phase < phases; phase++) {
                    System.out.println(String.format("Thread %s, phase %s", threadId, phase));
                    phaser.arriveAndAwaitAdvance();
                }
            });
            thread.start();
        }
    }
}
~~~
