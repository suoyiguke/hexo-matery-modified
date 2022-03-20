---
title: juc---线程池之ThreadPoolExecutor类用法.md
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
title: juc---线程池之ThreadPoolExecutor类用法.md
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
>闻道有先后，术业有专攻

java.util.concurrent.ThreadPoolExecutor 类是线程池的核心类，我们常常使用它来构建线程池，比如
> ExecutorService executorService = new ThreadPoolExecutor(2, 5, 2, TimeUnit.SECONDS, new LinkedBlockingQueue<>(3), Executors.defaultThreadFactory(), new ThreadPoolExecutor.AbortPolicy());

可以看到ThreadPoolExecutor 类是继承了实现ExecutorService 接口的AbstractExecutorService抽象类。因此ThreadPoolExecutor 提供的功可是要比ExecutorService 接口强大
![image.png](https://upload-images.jianshu.io/upload_images/13965490-de12f1ea1806980f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


它提供了ExecutorService 接口不具有的方法





######我们可以获得线程池的一些属性



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
            ThreadPoolExecutor threadPoolExecutor = (ThreadPoolExecutor) executorService;
            System.out.println("返回正在执行任务的线程的大概数量==>" + threadPoolExecutor.getActiveCount());
            System.out.println("池中核心线程数==>" + threadPoolExecutor.getCorePoolSize());
            System.out.println("在池中同时进行的最大线程数==>" + threadPoolExecutor.getLargestPoolSize());
            System.out.println("返回允许的最大线程数==>" + threadPoolExecutor.getMaximumPoolSize());
            System.out.println("返回池中当前的线程数 ==>" + threadPoolExecutor.getPoolSize());
            System.out.println("返回计划执行的任务的大概总数==>" + threadPoolExecutor.getTaskCount());
            System.out.println("返回完成执行的任务的大致总数==>" + threadPoolExecutor.getCompletedTaskCount());

            executorService.shutdown();
        }
    }
}
~~~

######启动所有核心线程

默认情况下，即使核心线程最初创建并且只有在新任务到达时才启动，但是可以使用方法prestartCoreThread()或prestartAllCoreThreads()动态地覆盖 。 如果您使用非空队列构建池，则可能需要预先提供线程。 

public int prestartAllCoreThreads()启动所有核心线程。
不需要在等任务到达之后才启动线程。 这将覆盖仅在执行新任务时启动核心线程的默认策略。 

~~~
package com.springboot.study.demo1;
import java.util.concurrent.*;
class Test1 {

    public static void main(String[] args) {
        //2个核心线程 等待数量席位3个  最大线程数5个，那么最大容纳任务是8个
        ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(2, 5, 2, TimeUnit.SECONDS, new LinkedBlockingQueue<>(3), Executors.defaultThreadFactory(), new ThreadPoolExecutor.AbortPolicy());
        System.out.println("池中核心线程数==>" + threadPoolExecutor.getCorePoolSize());
        System.out.println("返回池中当前的线程数 ==>" + threadPoolExecutor.getPoolSize());
        threadPoolExecutor.prestartAllCoreThreads();

        System.out.println("返回池中当前的线程数 ==>" + threadPoolExecutor.getPoolSize());

    }
}
~~~
调用prestartAllCoreThreads方法后，核心线程被启动，数量由0变成2
![image.png](https://upload-images.jianshu.io/upload_images/13965490-122c7a3679fdf6fd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



######设置核心线程的超时
我们知道线程池初始化后接到任务时就会保持一定数目的核心线程，默认是不会因为超时中断的。但是我们可以使用allowCoreThreadTimeOut方法来让核心线程超时中断。

public void allowCoreThreadTimeOut(boolean value)
如果为false，则由于缺少传入的任务，因此核心线程永远不会终止。
如果为true，则适用于非核心线程的相同的保持活动策略也适用于核心线程。为了避免连续替换线程，设置true时，保持活动时间必须大于零。通常应在主动使用池之前调用此方法。 

~~~
package com.springboot.study.demo1;
import java.util.concurrent.*;
class Test1 {

    public static void main(String[] args) {
        //2个核心线程 等待数量席位3个  最大线程数5个，那么最大容纳任务是8个
        ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(2, 5, 2, TimeUnit.SECONDS, new LinkedBlockingQueue<>(3), Executors.defaultThreadFactory(), new ThreadPoolExecutor.AbortPolicy());
        System.out.println("池中核心线程数==>" + threadPoolExecutor.getCorePoolSize());
        System.out.println("返回池中当前的线程数 ==>" + threadPoolExecutor.getPoolSize());
        //立马创建核心线程数量的线程
        threadPoolExecutor.prestartAllCoreThreads();
        System.out.println("返回池中当前的线程数 ==>" + threadPoolExecutor.getPoolSize());

        //允许核心线程超时
        threadPoolExecutor.allowCoreThreadTimeOut(true);
        //主线程睡眠3秒，等待核心线程超时。因为构造线程池时使用的 keepAliveTime是 2秒
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("返回池中当前的线程数 ==>" + threadPoolExecutor.getPoolSize());


    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-79922302fbe2ca8e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
