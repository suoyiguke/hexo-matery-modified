---
title: juc---CountDownLatch的使用和注意事项.md
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
title: juc---CountDownLatch的使用和注意事项.md
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
java.util.concurrent.CountDownLatch 是Doug Lea大师编写的juc包中的一个线程通信工具。

######使用场景一：实现多个线程在某个时间点同时执行
多个线程同时开始执行即是所谓的`并行`执行；这个功能我们使用CyclicBarrier也能实现，CyclicBarrier可以看看这篇 https://www.jianshu.com/p/aa4a86714291
~~~
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Test1 {
    //初始化计数器为1
    static CountDownLatch countDownLatch = new CountDownLatch(1);

    public static void main(String[] args) throws InterruptedException {
        //构建10个线程的定长线程池
        ExecutorService executorService = Executors.newFixedThreadPool(10);
        for (int i = 0; i < 10; i++) {
            executorService.submit(new Runnable() {
                @Override
                public void run() {
                    try {
                        //等待
                        countDownLatch.await();
                        System.out.println("Thread:" + Thread.currentThread().getName() + ",time: " + System.currentTimeMillis());
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            });
        }
        //计数器减一，为0时等待的线程开始执行
        countDownLatch.countDown();


    }
}
~~~
######使用场景二：一个线程等待其它多个线程执行完毕后再开始执行

同样CyclicBarrier也能实现，不过CyclicBarrier是提供一个回调方法。最终执行这个回调方法的线程是最后到达屏障的线程。这个功能还是和CountDownLatch有所区别的。CountDownLatch的`一个线程`是调用   countDownLatch.countDown();方法的线程而不属于多个线程中的任意一个
~~~
import java.util.concurrent.CountDownLatch;

public class Test2 {
    public static void main(String[] args) throws InterruptedException {
        //初始化计数器为5
        int threadCount = 5;
        final CountDownLatch latch = new CountDownLatch(threadCount);
        //同样线程数量也为5
        for (int i = 0; i < threadCount; i++) {
            Thread thread = new Thread(new Runnable() {

                @Override
                public void run() {
                    try {
                        Thread.sleep(3*1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    System.out.println("执行子线程...");
                    //计数器减一
                    latch.countDown();
                }

            });
            thread.start();

        }
        //主线程等待
        latch.await();
        System.out.println("执行主线程...");
    }

}
~~~
###关键方法
- CountDownLatch latch = new CountDownLatch(10); 构造器，指定计数器初始化为10
- latch.getCount() 获得当前计数器数量
-  latch.countDown() 计数器减一
-  latch.await() 线程等待，只到计数器为0便继续执行

![image.png](https://upload-images.jianshu.io/upload_images/13965490-453021031caecf39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######CountDownLatch的注意事项
《阿里巴巴Java开发手册》中对于CountDownLatch的使用有如下规定：
>【推荐】 使用 CountDownLatch 进行异步转同步操作，每个线程退出前必须调用 countDown方法，线程执行代码注意 catch 异常，确保 countDown 方法被执行到，避免主线程无法执行至 await 方法，直到超时才返回结果。
说明：注意，子线程抛出异常堆栈，不能在主线程 try-catch 到。


举个例子如下
~~~
package io.renren;

import java.text.ParseException;
import java.util.concurrent.*;

public class ScheduledExecutorServiceTest {


    public static void main(String[] args) throws InterruptedException {


        CountDownLatch countDownLatch = new CountDownLatch(2);
        new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println(Thread.currentThread().getName());
                countDownLatch.countDown();

            }
        },"A").start();

        new Thread(new Runnable() {
            @Override
            public void run() {

                int i =  1/0;
                System.out.println(Thread.currentThread().getName());
                countDownLatch.countDown();

            }
        },"B").start();

        countDownLatch.await();
        System.out.println("main线程结束");
    }
}
~~~
运行程序，线程B因为出现可除0异常，而且没有捕获。呆滞后面的  countDownLatch.countDown(); 减计数方法没有的得到执行。所以main线程将一直等待阻塞下去！

所以我们需要try/catch 包裹线程内业务代码，并且在finally 中调用countDown方法，防止主线程永久阻塞下去
~~~
package io.renren;
import java.text.ParseException;
import java.util.concurrent.*;
public class ScheduledExecutorServiceTest {

    public static void main(String[] args) throws InterruptedException {
        CountDownLatch countDownLatch = new CountDownLatch(2);
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                   System.out.println(Thread.currentThread().getName());
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    countDownLatch.countDown();
                }

            }
        }, "A").start();

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    int i = 1 / 0;
                    System.out.println(Thread.currentThread().getName());
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    countDownLatch.countDown();
                }

            }
        }, "B").start();
        countDownLatch.await();
        System.out.println("main线程结束");
    }
}
~~~
