---
title: juc---Atomic原子类之使用LongAdder代替AtomicLong.md
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
title: juc---Atomic原子类之使用LongAdder代替AtomicLong.md
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
> 不在其位，不谋其政

《阿里巴巴Java开发手册》里面有提到：

>【参考】 volatile 解决多线程内存不可见问题。对于一写多读，是可以解决变量同步问题，但是如果多写，同样无法解决线程安全问题。
说明：如果是 count++操作，使用如下类实现：AtomicInteger count = new AtomicInteger(); count.addAndGet(1); 如果是 JDK8，推荐使用 LongAdder 对象，比 AtomicLong 性能更好（减少乐观锁的重试次数）。

手册推荐我们使用LongAdder 类代替AtomicLong类。LongAdder 相对于AtomicLong 在高并发下的表现非常好。而且在较低并发下LongAdder 的性能和AtomicLong 差不多，只是LongAdder 的内存消耗比AtomicLong 要高。因为阅读LongAdder 源码可得，它其实是使用一种`空间换时间`的手段来提供性能的，它内部维护了一个数组。

######下面做实验来对比AtomicLong和LongAdder的迭加性能

使用线程池开启8个线程，线程开多了也没有用，因为我的机器cpu是8核的，同时只允许8个线程并发执行。所以我们分别对LongAdder和 AtomicLong做 1000000000l 次迭加，看看耗时多少。

先来看LongAdder的执行时间
~~~
package io.renren;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicIntegerArray;
import java.util.concurrent.atomic.LongAdder;
/**
 *@description: Test_Automic
 *@author: yinkai
 *@create: 2020/3/18 21:55
 */
public class Test_Automic {
    static long startTime = 0;
    static ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(
            8, 8, 10, TimeUnit.SECONDS,
            new ArrayBlockingQueue<>(1),
            Executors.defaultThreadFactory(),
            new ThreadPoolExecutor.AbortPolicy());
    public static void main(String[] args) {

        CyclicBarrier cyclicBarrier = new CyclicBarrier(8, new Runnable() {
            @Override
            public void run() {
                //结束计时
                long endTime =  System.currentTimeMillis();
                long usedTime = endTime- startTime;
                System.out.println("执行毫秒数 "+usedTime);
                threadPoolExecutor.shutdown();
            }
        });
        LongAdder longAdder = new LongAdder();
        //开始计时
        startTime = System.currentTimeMillis();
        for (int i = 0; i < 8; i++) {
            threadPoolExecutor.submit(new Runnable() {
                @Override
                public void run() {

                    for (int i = 0; i < 1000000000l; i++) {
                        longAdder.increment();
                    }
                    try {
                        cyclicBarrier.await();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            });
        }
    }
}
~~~
执行上面的程序，得出耗时为 18201毫秒
![image.png](https://upload-images.jianshu.io/upload_images/13965490-993bc8988bbe9e6d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

再来看AtomicLong的执行迭加时间
~~~
package io.renren;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;
/**
 *@description: Test_Automic
 *@author: yinkai
 *@create: 2020/3/18 21:55
 */
public class Test_Automic {
    static long startTime = 0;
    static ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(
            8, 8, 10, TimeUnit.SECONDS,
            new ArrayBlockingQueue<>(1),
            Executors.defaultThreadFactory(),
            new ThreadPoolExecutor.AbortPolicy());

    public static void main(String[] args) {

        CyclicBarrier cyclicBarrier = new CyclicBarrier(8, new Runnable() {
            @Override
            public void run() {
                //结束计时
                long endTime =  System.currentTimeMillis();
                long usedTime = endTime- startTime;
                System.out.println("执行毫秒数 "+usedTime);

                threadPoolExecutor.shutdown();
            }
        });
        AtomicLong atomicLong = new AtomicLong();
        //开始计时
        startTime = System.currentTimeMillis();
        for (int i = 0; i < 8; i++) {
            threadPoolExecutor.submit(new Runnable() {
                @Override
                public void run() {

                    for (int i = 0; i < 1000000000l; i++) {
                        atomicLong.getAndIncrement();
                    }
                    try {
                        cyclicBarrier.await();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            });
        }
    }
}
~~~
AtomicLong 执行以上迭加耗时164516 毫秒 多出了接近10倍的时间。。
![image.png](https://upload-images.jianshu.io/upload_images/13965490-0360e893cc1e2b49.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


######LongAdder为什么比AtomicLong快这么多？

