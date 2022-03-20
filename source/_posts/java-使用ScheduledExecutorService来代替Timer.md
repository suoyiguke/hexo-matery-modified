---
title: java-使用ScheduledExecutorService来代替Timer.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: java基础
categories: java基础
---
> 志存高远

《阿里巴巴Java开发手册》中有关于Timer和ScheduledExecutorService的用法说明如下
>【强制】 多线程并行处理定时任务时，Timer 运行多个 TimeTask 时，只要其中之一没有捕获抛出的异常，其它任务便会自动终止运行，如果在处理定时任务时使用ScheduledExecutorService 则没有这个问题。

它要求使用ScheduledExecutorService来代替Timer

###先来看Timer



我们来看下列程序


~~~
package io.renren;
import java.util.Timer;
import java.util.TimerTask;

public class TimerTest {


    public static void main(String[] args) {
        Timer timer = new Timer();

        /**
         * 3秒打印一次线程名
         */
        timer.schedule(new TimerTask() {
            @Override
            public void run() {

                System.out.println("==="+Thread.currentThread().getName()+"===");
            }
        },0,3*1000);

        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                System.out.println("***"+Thread.currentThread().getName()+"***");

            }
        },0,3*1000);

    }
}
~~~
一个Timer运行了2个TimerTask，TimerTask的run方法每3秒执行一次。打印了执行run方法的线程名；可以看到它们是使用同一个`Timer-0`线程来执行任务的
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c90e4d9d5906bbbc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

######Timer的任务出现异常可能导致其他任务不被执行
因为Timer总是使用单个线程来执行多个TimerTask的，这样一个TimerTask抛出异常会影响到其它TimerTask的执行 ~
如下给 其中一个抛出一个运行时异常看看会怎么样呢？
~~~
package io.renren;
import java.util.Timer;
import java.util.TimerTask;
public class TimerTest {
    public static void main(String[] args) {
        Timer timer = new Timer();

        /**
         * 3秒打印一次线程名
         */
        timer.schedule(new TimerTask() {
            @Override
            public void run() {

                System.out.println("==="+Thread.currentThread().getName()+"===");
            }
        },0,3*1000);

        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                int i = 1/0;
                System.out.println("***"+Thread.currentThread().getName()+"***");
            }
        },0,3*1000);

    }
}
~~~
运行上面程序古，可以看到线程直接退出了
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c2546a27aa86b6cf.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


>TimerTask抛出的未检查的异常会终止timer线程，此后已经被安排但尚未执行的TimerTask永远不会再执行了，新的任务也不能被调度了

######执行耗时的TimerTask会影响其它TimerTask的执行
我们再来看如下例子


~~~
package io.renren;
import java.sql.Time;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.TimeUnit;
public class TimerTest {
    public static void main(String[] args) {
        Timer timer = new Timer();

        /**
         * 3秒打印一次线程名
         */
        timer.schedule(new TimerTask() {
            @Override
            public void run() {

            System.out.println("==="+Thread.currentThread().getName()+"===");
                try {
                    TimeUnit.SECONDS.sleep(10);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        },0,3*1000);
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                System.out.println("***"+Thread.currentThread().getName()+"***");
            }
        },0,3*1000);

    }
}
~~~
执行程序就会发现第二个TimerTask迟迟得不到执行。这也是Timer的单线程执行导致的缺点

>创建Timer的时候会创建TimerThread做为执行线程，所以一个Timer对应一个线程，如果一个TimerTask执行的时间过长，其他的TimerTask只能等待。

######Timer的执行时基于系统的绝对时间的
如果系统的绝对时间被改变，那么Timer的执行将被影响！

如下程序，设定等到2020-03-18 10:04:00 时就会触发调用TimerTask。如果我在之前将系统的时间修改，那么改程序就无法得到准确的执行了。

我将时间修改为 2020-03-17 日。今天其实是18日。执行下列程序。就发现TimerTask迟迟得不到执行

~~~
package io.renren;
import java.sql.Time;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.TimeUnit;
public class TimerTest {
    public static void main(String[] args) throws ParseException {
        Timer timer = new Timer();
        SimpleDateFormat ft = new SimpleDateFormat ("yyyy-MM-dd hh:mm:ss");
        Date parse = ft.parse("2020-03-18 10:04:00");

        /**
         * 3秒打印一次线程名
         */
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
               System.out.println("==="+Thread.currentThread().getName()+"===");
                try {
                    TimeUnit.SECONDS.sleep(10);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, parse);
    }
}
~~~
>Timer对调度的支持是基于绝对时间的，对系统时钟的改变是敏感的


###我们再来看ScheduledExecutorService
ScheduledExecutorService没有timer的上面说名的三个缺陷。
它是多线程执行任务的，可以指定初始化线程数（因为它本身是使用线程池ThreadPoolExecutor实现的）


我们来看下面代码，即使在第二次提交Runnable时出现了除0异常，也不会影响到第一次提交的Runnable执行
~~~
package io.renren;

import java.text.ParseException;
import java.util.concurrent.*;

public class ScheduledExecutorServiceTest {


    public static void main(String[] args) {

        ScheduledExecutorService scheduledExecutorService = Executors.newScheduledThreadPool(2);
        scheduledExecutorService.scheduleAtFixedRate(
                new Runnable() {
                    @Override
                    public void run() {
                        System.out.println("===" + Thread.currentThread().getName() + "===");
                    }
                }
                , 0, 3, TimeUnit.SECONDS);


        scheduledExecutorService.scheduleAtFixedRate(
                new Runnable() {
                    @Override
                    public void run() {
                        int i = 1/0;
                        System.out.println("***" + Thread.currentThread().getName() + "***");
                    }
                }
                , 0, 3, TimeUnit.SECONDS);


    }
}
~~~

再来看是否因为某个Runnable执行时长过长导致其他Runnable延迟执行
~~~
package io.renren;

import java.text.ParseException;
import java.util.concurrent.*;

public class ScheduledExecutorServiceTest {


    public static void main(String[] args) {

        ScheduledExecutorService scheduledExecutorService = Executors.newScheduledThreadPool(2);
        scheduledExecutorService.scheduleAtFixedRate(
                new Runnable() {
                    @Override
                    public void run() {
                        System.out.println("===" + Thread.currentThread().getName() + "===");
                        try {
                            TimeUnit.SECONDS.sleep(10);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                }
                , 0, 3, TimeUnit.SECONDS);


        scheduledExecutorService.scheduleAtFixedRate(
                new Runnable() {
                    @Override
                    public void run() {
                        System.out.println("***" + Thread.currentThread().getName() + "***");
                    }
                }
                , 0, 3, TimeUnit.SECONDS);
    }
}
~~~
执行上面程序，可以看到打印了多次 pool-1-thread-2。说明这个问题在ScheduledExecutorService 中不会出现
![image.png](https://upload-images.jianshu.io/upload_images/13965490-3d00cc5267c8fe58.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


ScheduledExecutorService 是基于`相对时间`的，这点也不同于Timer。因此不会出现修改系统时间，指定运行的任务也跟着影响的尴尬局面了
