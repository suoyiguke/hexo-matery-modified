---
title: synchronized的可重入性.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jmm
categories: jmm
---
---
title: synchronized的可重入性.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jmm
categories: jmm
---
从互斥锁的设计上来说，当一个线程试图操作一个由其他线程持有的对象锁的临界资源时，将会处于阻塞状态，**但当一个线程再次请求自己持有对象锁的临界资源时，这种情况属于重入锁，请求将会成功**，在java中synchronized是基于原子性的内部锁机制，是可重入的，因此在一个线程调用synchronized方法的同时在其方法体内部调用该对象另一个synchronized方法，**也就是说一个线程得到一个对象锁后再次请求该对象锁，是允许的，这就是synchronized的可重入性**。如下：
~~~
import java.util.ArrayList;
import java.util.List;
public class AccountingSync implements Runnable {
    static AccountingSync instance = new AccountingSync();
    static int i = 0;
    static int j = 0;

    @Override
    public void run() {
        for (int j = 0; j < 1000000; j++) {

            //this,当前实例对象锁
            synchronized (this) {
                i++;
                increase();//synchronized的可重入性
            }
        }
    }

    public synchronized void increase() {
        j++;
    }


    public static void main(String[] args) throws InterruptedException {

        List<Thread> threads = new ArrayList<>(10);
        for (int k = 0; k < 10; k++) {
            Thread thread = new Thread(instance);
            thread.start();
            threads.add(thread);
        }

        for (Thread thread : threads) {
            thread.join();
        }

        System.out.println(i);
        System.out.println(j);
    }
}
~~~
正如代码所演示的，在获取当前实例对象锁后进入synchronized代码块执行同步代码，并在代码块中调用了当前实例对象的另外一个synchronized方法，再次请求当前实例锁时，将被允许，进而执行方法体代码，这就是重入锁最直接的体现。

>如果synchronized不可重入，increase()方法执行将一直阻塞下去。造成死锁！



需要特别注意另外一种情况，当子类继承父类时，子类也是可以通过可重入锁调用父类的同步方法。注意由于synchronized是基于monitor实现的，因此每次重入，monitor中的计数器仍会加1。

>子类如果想要重写父类的同步方法，synchronized关键字一定要显示写出，否则无效。

