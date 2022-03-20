---
title: juc---线程池之基本概念.md
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
title: juc---线程池之基本概念.md
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
###为什么使用线程池？
线程池的优势：
线程池做的工作只要是控制运行的线程数量，处理过程中将任务放入队列，然后在线程创建后启动这些任务，如果线程数量超过了最大数量，超出数量的线程排队等候，等其他线程执行完毕，再从队列中取出任务来执行。
 
它的主要特点为：`线程复用`;控制最大并发数;管理线程。
 
第一：降低资源消耗。通过重复利用已创建的线程降低线程创建和销毁造成的销耗。
第二：提高响应速度。当任务到达时，任务可以不需要等待线程创建就能立即执行。
第三：提高线程的可管理性。线程是稀缺资源，如果无限制的创建，不仅会销耗系统资源，还会降低系统的稳定性，使用线程池可以进行统一的分配，调优和监控。
 
 
 ######线程池能让线程复用
我们知道，在java中一个线程start后不能再次start。关于这个问题我的这篇博客有讲解：https://www.jianshu.com/p/a2c3ba1c1e72
如果使用线程池，那么这个问题就迎刃而解了。线程池能让线程重复使用！这样就不用重复去创建线程和销毁线程了。降低了资源消耗


我们想通过子线程执行一个任务， 把业务逻辑写在线程的run方法里。要等到线程创建完毕后才能start开始执行。如果使用线程池，当任务到达时，任务可以不需要等待线程创建就能立即执行。

###线程池接口
![image.png](https://upload-images.jianshu.io/upload_images/13965490-751c8c57a77a731d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- 线程池的核心类是 java.util.concurrent.ThreadPoolExecutor
- 线程池核心接口是 java.util.concurrent.ExecutorService 
- 线程的工具类 java.util.concurrent.Executors


###三种线程池
不推荐使用Executors工具类构造的三种线程池，这里只是了解一下。真正的使用我的这篇文章有提到：https://www.jianshu.com/p/d55d3f520b82

######Executors.newFixedThreadPool(e);
`一池指定数量线程`
newFixedThreadPool创建的线程池corePoolSize和maximumPoolSize值是相等的，它使用的是LinkedBlockingQueue

~~~
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Test {

    public static void main(String[] args) {
        ExecutorService executorService = Executors.newFixedThreadPool(5);
        try {
            for (int i = 0; i < 10; i++) {

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
看看执行结果：pool-1-thread-1 线程被多次使用。说明线程池中的线程并不是公平的执行，而是谁先执行完，立马可以再次执行
![image.png](https://upload-images.jianshu.io/upload_images/13965490-ac7908a741309b53.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######Executors.newSingleThreadExecutor();
`一池一线程`
newFixedThreadPool创建的线程池corePoolSize和maximumPoolSize值是相等的，它使用的是LinkedBlockingQueue
~~~
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Test {

    public static void main(String[] args) {
        ExecutorService executorService = Executors.newSingleThreadExecutor();
        try {
            for (int i = 0; i < 10; i++) {

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

######Executors.newCachedThreadPool();
`一池n线程`  适合执行很多短期异步任务。线程池根据需要创建新线程，但在先前就构建的线程空闲时优先重用。可自动扩容，遇强则强

newCachedThreadPool创建的线程池将corePoolSize设置为0，将maximumPoolSize设置为Integer.MAX_VALUE，它使用的是SynchronousQueue，也就是说来了任务就创建线程运行，当线程空闲超过60秒，就销毁线程


~~~
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Test {

    public static void main(String[] args) {
        ExecutorService executorService = Executors.newCachedThreadPool();
        try {
            for (int i = 0; i < 10; i++) {

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
执行结果： newCachedThreadPool为每个任务都创建了对应的线程，并没有重用线程。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fcece64fecda9733.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
原因是速度太快了，我们可以sleep一下
~~~
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Test {

    public static void main(String[] args) {
        ExecutorService executorService = Executors.newCachedThreadPool();
        try {
            for (int i = 0; i < 10; i++) {
                try {
                    TimeUnit.SECONDS.sleep(1);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
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
这样newCachedThreadPool并没有创建新线程，只是使用一个线程完成所有任务！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7a9cbdf00a7c167a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
