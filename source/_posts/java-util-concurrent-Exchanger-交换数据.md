---
title: java-util-concurrent-Exchanger-交换数据.md
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
title: java-util-concurrent-Exchanger-交换数据.md
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
Exchanger 是 JDK 1.5 开始提供的一个用于两个工作线程之间交换数据的封装工具类。

**简单说就是一个线程在完成一定的事务后想与另一个线程交换数据，则第一个先拿出数据的线程会一直等待第二个线程，直到第二个线程拿着数据到来时才能彼此交换对应数据。**
其定义为 Exchanger<V> 泛型类型，其中 V 表示可交换的数据类型，对外提供的接口很简单，具体如下：



~~~
        Exchanger<Integer> exchanger = new Exchanger<>();

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                try {
                    Object exchange = exchanger.exchange(0);
                    System.out.println("线程A 打印"+exchange);

                } catch (InterruptedException e) {
                    e.printStackTrace();
                }


            }
        },"A").start();



        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                try {
                    Object exchange = exchanger.exchange(1);
                    System.out.println("线程B 打印"+exchange);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

            }
        },"B").start();
~~~
