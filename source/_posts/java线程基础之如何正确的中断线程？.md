---
title: java线程基础之如何正确的中断线程？.md
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
title: java线程基础之如何正确的中断线程？.md
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
线程中断情况不同，有两种方法

目标线程检测到isInterrupted()为true
~~~
public class Main {

    public static void main(String[] args) throws InterruptedException {
        HelloThread t = new HelloThread();
        t.start();
        Thread.sleep(1);
        t.interrupt();
        System.out.println("end");
    }
}

class HelloThread extends Thread {

    @Override
    public void run() {
        int n = 0;
        while (!isInterrupted()) {
            n++;
            System.out.println(n + " hello!");
        }
    }
}

~~~




2、当处于暂停之中时，捕获了InterruptedException都应该立刻结束自身线程；

~~~
public class Main {

    public static void main(String[] args) throws InterruptedException {
        HelloThread t = new HelloThread();
        t.start();
        Thread.sleep(1);
        t.interrupt();
        System.out.println("end");
    }
}

class HelloThread extends Thread {

    @Override
    public void run() {
        int n = 0;
        while (!isInterrupted()) {
            n++;
            System.out.println(n + " hello!");
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                break;
            }
        }
    }
}


~~~
