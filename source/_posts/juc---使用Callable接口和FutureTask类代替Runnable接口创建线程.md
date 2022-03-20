---
title: juc---使用Callable接口和FutureTask类代替Runnable接口创建线程.md
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
title: juc---使用Callable接口和FutureTask类代替Runnable接口创建线程.md
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
我们说，在Java中传统的创建线程方式有两种： 继承Thread和实现Runnable接口
我的这篇文有具体介绍两种方式 ：https://www.jianshu.com/p/a2c3ba1c1e72
而JUC给我们提供了更强大的接口==> Callable
它与Runnable相比，能够获取子线程的异步执行结果！


######使用Callable接口构造线程

![image.png](https://upload-images.jianshu.io/upload_images/13965490-cf0680d9392dbfd1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

java中要构造线程需要实现Runnable接口，Runnable做为一个中介。既可以将Runnable接口传入Thread的构造器，又可以将实现Runnable的类传入构造器。而这里还需要实现Callable接口，所以需要一个类即实现Runnable又实现了Callable。
juc下的 FutureTask类正好可以用在这！这其实是java中的一个`多态思想` 通过面向接口编程的形式的体现

######使用Callable接口配合FutureTask类创建线程，获得A线程异步的执行结果
~~~
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;

class TestLock {

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        FutureTask futureTask = new FutureTask(new Callable() {
            @Override
            public String call() throws Exception {
                return "hello Callable and FutureTask!!";
            }
        });
        new Thread(futureTask,"A").start();
        String str = (String) futureTask.get();
        System.out.println(str);
    }
}
~~~

######`细节`FutureTask只会执行一次
如果FutureTask先后和A、B两个线程绑定，那么只有先执行的A线程会得到执行，B线程会直接复用A线程的执行结果！

~~~
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;

class TestLock {
    static int i = 0;

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        FutureTask futureTask = new FutureTask(new Callable() {
            @Override
            public String call() throws Exception {
                i++;
                System.out.println("执行FutureTask的call！");

                return "hello Callable and FutureTask!!";
            }
        });


        new Thread(futureTask,"A").start();
        String str1 = (String) futureTask.get();
        System.out.println(str1);

        new Thread(futureTask,"B").start();
        String str2 = (String) futureTask.get();
        System.out.println(str2);

        System.out.println("FutureTask的call执行了"+i+"次");


    }
}
~~~

执行结果
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a4f8a6647b4c0a80.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######Future接口的方法解析
1、get()方法是阻塞的，调用此方法的线程将会等待子线程执行完毕，返回值即是子线程Callable接口的call方法的返回值

2、cancel()方法用来取消任务，如果取消任务成功则返回true，如果取消任务失败则返回false。
- 参数mayInterruptIfRunning表示是否允许取消正在执行却没有执行完毕的任务，`如果设置true，则表示可以取消正在执行过程中的任务。`
①、如果任务已经完成，则无论mayInterruptIfRunning为true还是false，此方法肯定返回false，即如果取消已经完成的任务会返回false；
②、正在执行的任务，若mayInterruptIfRunning为true直接停止掉，返回true。设置为false就不会去停止了，返回false
③、如果任务还没有执行，则无论mayInterruptIfRunning为true还是false，肯定返回true。(还没开始的任务直接干掉，返回true)
`换句话说，mayInterruptIfRunning设为false的话无法结束正在执行的任务。想要直接干掉运行状态的任务请使用 futureTask.cancel(true);`



3、isCancelled()方法表示任务是否被取消成功，如果在任务正常完成前被取消成功，则返回 true。

4、isDone()表示任务是否已经完成，则返回true，注意：正常完成、异常 或 取消操作都代表任务完成。判断任务状态使用这个isDone()就行了，isCancelled()针对于取消！

5、get(long timeout, TimeUnit unit)用来获取执行结果，如果在指定时间内，还没获取到结果，就直接返回null。

######使用FutureTask来中断正在执行的任务
核心代码
~~~
 //判断有没有执行完毕，没有执行完毕则取消任务
        if (!futureTask.isDone()) {
            futureTask.cancel(true);
        }
~~~

~~~
import java.util.concurrent.Callable;
import java.util.concurrent.FutureTask;
import java.util.concurrent.TimeUnit;

class TestLock {

    public static void main(String[] args) throws InterruptedException {

        FutureTask futureTask = new FutureTask(new Callable() {
            @Override
            public String call() throws Exception {
                System.out.println("开始执行子线程");
                System.out.println("sleep 10秒");
                TimeUnit.SECONDS.sleep(10);
                System.out.println("结束执行！");

                return "hello Callable and FutureTask!!";
            }
        });
        new Thread(futureTask, "A").start();
        TimeUnit.SECONDS.sleep(2);

        //判断有没有执行完毕，没有执行完毕则取消任务
        if (!futureTask.isDone()) {
            futureTask.cancel(true);
        }
    }
}
~~~
运行结果：只会打印sleep 10秒前的输出，    System.out.println("结束执行！");没有得到执行，说明线程被中断！
![image.png](https://upload-images.jianshu.io/upload_images/13965490-181ecd1b2ea0a95c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######FutureTask和线程池一起使用示例
~~~
package com.springboot.study.demo1;

import java.util.concurrent.*;

class Test1 {

    public static void main(String[] args) throws InterruptedException {
        ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(2, 5, 2, TimeUnit.SECONDS, new LinkedBlockingQueue<>(3), Executors.defaultThreadFactory(), new ThreadPoolExecutor.AbortPolicy());

        FutureTask<Integer> future = new FutureTask<Integer>(
                new Callable<Integer>() {
                    @Override
                    public Integer call() throws InterruptedException {
                        System.out.println("执行子线程");
                        //失眠3秒
                        TimeUnit.SECONDS.sleep(3);

                        return 1;
                    }
                }
        );
        threadPoolExecutor.submit(future);

        TimeUnit.SECONDS.sleep(1);
        if(!future.isDone()){
            future.cancel(true);
            System.out.println("任务被中断执行");
            System.out.println("返回池中当前的线程数 ==>" + threadPoolExecutor.getPoolSize());

        }


        threadPoolExecutor.shutdown();

    }
}
~~~
