---
title: juc---线程池之七大参数介绍和正确的构造线程池.md
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
title: juc---线程池之七大参数介绍和正确的构造线程池.md
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
###线程池之七大参数
我们知道，线程池的核心类是 ThreadPoolExecutor，构造一个ThreadPoolExecutor需要7个参数！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-04d9c4aac3e267af.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######int corePoolSize
线程池中的常驻核心线程数

######int maximumPoolSize
线程池中能够容纳同时执行的最大线程数，此值必须大于等于1

######long keepAliveTime

多余的空闲线程的存活时间。当前池中的线程数量超过corePoolSize时，多余线程会被销毁到只剩下corePoolSize个线程为至

######TimeUnit unit
keepAliveTime的单位

######BlockingQueue<Runnable> workQueue
任务队列，被提交但未被执行的任务。由阻塞队列实现，关于阻塞队列我这篇文章有讲解 https://www.jianshu.com/p/862c93ab3203

######ThreadFactory threadFactory
表示生产线程池中工作线程的工厂。用于创建线程，`一般默认即可`


######RejectedExecutionHandler handler
拒绝策略，表示当队列满了，并且工作线程大于等于线程池的最大线程数（maximumPoolSize）时如何来拒绝请求执行的runnable饿策略。
我的这篇文章有详细的讲解拒绝策略
https://www.jianshu.com/p/bf6fabb7b459

###实际上我们应该如何使用线程池？
不允许直接使用jdk自带的三种线程池
~~~
Executors.newCachedThreadPool();
Executors.newFixedThreadPool(5);
Executors.newSingleThreadExecutor();
~~~
工作中请使用自定义的写法：直接使用ThreadPoolExecutor类带上7个参数构造线程池！因为可能导致oom异常，所谓oom异常就是 `java.lang.OutOfMemoryError:Java heap space`
![image.png](https://upload-images.jianshu.io/upload_images/13965490-1929680166ec5269.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######实际上请使用ThreadPoolExecutor类带上7个参数来构造线程池
- 注意指定队列的长度，我这里是new LinkedBlockingQueue<>(3)。如果不指定3，则队列长度为`Integer.MAX_VALUE`,可能因为任务的积累导致oom。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a1194cb450e9edec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- maximumPoolSize在cpu密级型项目中请配置成 `cup核心数+1`==>Runtime.getRuntime().availableProcessors()+1 
 maximumPoolSize在io密级型项目中请配置成 `cpu核心数/阻塞系数`


###参数调整试验
使用如下代码来构造线程池。2个核心线程，5个最大数量，3个等待队列席位。
~~~
        ExecutorService executorService =
                new ThreadPoolExecutor(
                        2,
                        5,
                        2, TimeUnit.SECONDS,
                        new LinkedBlockingQueue<>(3),
                        Executors.defaultThreadFactory(),
                        new ThreadPoolExecutor.AbortPolicy());
~~~


######实验一，任务数量为6
~~~
import java.util.concurrent.*;

public class Test {

    public static void main(String[] args) {
        ExecutorService executorService = new ThreadPoolExecutor(2, 5, 2, TimeUnit.SECONDS, new LinkedBlockingQueue<>(3), Executors.defaultThreadFactory(), new ThreadPoolExecutor.AbortPolicy());
        try {
            for (int i = 1; i <= 6; i++) {
                executorService.execute(new Runnable() {
                    @Override
                    public void run() {
                        System.out.println(Thread.currentThread().getName() + " 办理业务");
                    }
                });
            }
        } finally {
            executorService.shutdown();
        }

    }
}
~~~
这里有6个任务。所以线程池的核心线程、等待队列都被用完。还剩下1个任务（6-2-3=1），需要创建线程来执行。所以执行结果中打印了pool-1-thread-3，该线程即是线程池临时创建出来的线程!
![image.png](https://upload-images.jianshu.io/upload_images/13965490-47a3881c1547489e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######实验二，任务数量为9
~~~
package com.springboot.study.demo1;
import java.util.concurrent.*;
class Test1 {

    public static void main(String[] args) {
        //2个核心线程 等待数量席位3个  最大线程数5个，那么最大容纳任务是8个
        ExecutorService executorService = new ThreadPoolExecutor(2, 5, 2, TimeUnit.SECONDS, new LinkedBlockingQueue<>(3), Executors.defaultThreadFactory(), new ThreadPoolExecutor.AbortPolicy());
        try {
            //提交9次任务，超出的1个任务会被应用拒绝策略
            for (int i = 1; i <= 9; i++) {
                executorService.execute(new Runnable() {
                    @Override
                    public void run() {
                        System.out.println(Thread.currentThread().getName() + " 办理业务");
                    }
                });
            }
        } finally {
            executorService.shutdown();
        }
    }
}
~~~
执行结果：抱错。此时任务数量9超过线程池可接受的最大任务数8（maximumPoolSize 3 +workQueue的容量5）

>Exception in thread "main" java.util.concurrent.RejectedExecutionException: Task Test$1@42110406 rejected from java.util.concurrent.ThreadPoolExecutor@531d72ca[Running, pool size = 5, active threads = 5, queued tasks = 3, completed tasks = 0]


######创建自定义线程工厂为线程池中线程命名
 创建线程池时使用自定义的线程工厂，这样可以为该线程池内的线程改名
~~~
package io.renren;

import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class UserThreadFactory implements ThreadFactory {
    private final String namePrefix;
    private final AtomicInteger nextId = new AtomicInteger(1);
    // 定义线程组名称，在 jstack 问题排查时，非常有帮助
     public UserThreadFactory(String whatFeaturOfGroup) {
        namePrefix = "来自 UserThreadFactory 线程工厂的 " + whatFeaturOfGroup + "-线程-";
    }
    @Override
    public Thread newThread(Runnable task) {
        String name = namePrefix + nextId.getAndIncrement();
        Thread thread = new Thread(null, task, name, 0);
        System.out.println(thread.getName());
        return thread;
    }
}

class TestFa{

    public static void main(String[] args) {

        UserThreadFactory userThreadFactory = new UserThreadFactory(" 用户 ");

        ThreadPoolExecutor threadPoolExecutor =
                new ThreadPoolExecutor(
                        2,
                        5,
                        2, TimeUnit.SECONDS,
                        new LinkedBlockingQueue<>(3),
                        userThreadFactory ,
                        new ThreadPoolExecutor.AbortPolicy());

        for (int i = 0; i <8 ; i++) {
            threadPoolExecutor.submit(new Runnable() {
                @Override
                public void run() {
                    System.out.println(Thread.currentThread().getName());
                }
            });
        }

        threadPoolExecutor.shutdown();


    }

}
~~~



######ThreadFactory 匿名
~~~
        ThreadFactory threadFactory = new ThreadFactory() {
            AtomicInteger nextId = new AtomicInteger(1);
            @Override
            public Thread newThread(Runnable task) {
                Thread thread = new Thread(null, task, "测试redis分布式锁线程" + nextId.getAndIncrement(), 0);
                return thread;
            }
        };

        ThreadPoolExecutor threadPoolExecutor =
                new ThreadPoolExecutor(2,
                        5,
                        3,
                        TimeUnit.MINUTES,
                        new ArrayBlockingQueue<>(5),
                        threadFactory,
                        new ThreadPoolExecutor.AbortPolicy()
                );

        for (int i = 0; i <10 ; i++) {
            threadPoolExecutor.submit(new Runnable() {
                @Override
                public void run() {

                    System.out.println(Thread.currentThread().getName());

                }
            });
        }
~~~

###构造一个单线程池的实例
~~~
    private static ExecutorService executorService =

        new ThreadPoolExecutor(1, 1,
            0L, TimeUnit.MILLISECONDS,
            new LinkedBlockingQueue<>(),
            r -> new Thread(null, r, "check-redis-thread", 0),
            new ThreadPoolExecutor.AbortPolicy());
~~~
