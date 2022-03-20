---
title: juc---Atomic原子类之基本类型的原子更新（一）.md
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
title: juc---Atomic原子类之基本类型的原子更新（一）.md
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

> 使用原子的方式更新基本类型，Atomic包提供了以下3个类。
> - AtomicBoolean：原子更新布尔类型。
> - AtomicInteger：原子更新整型。
> - AtomicLong：原子更新长整型。



以上3个类提供的方法几乎一模一样，就以AtomicLong为例看看它的用法吧。


###原子设定值
######set
设置为给定值。

######lazySet
最终设定为给定值。 


###原子加1和减1

~~~
package io.renren;

import java.util.concurrent.Executors;
import java.util.concurrent.SynchronousQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicLong;

/**
 *@description: Test_Automic
 *@author: yinkai
 *@create: 2020/3/18 21:55
 */
public class Test_Automic {

    static ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(
            8,8,
            10, TimeUnit.SECONDS,
            new SynchronousQueue(),
            Executors.defaultThreadFactory(),
            new ThreadPoolExecutor.AbortPolicy()
    );


    public static void main(String[] args) {

        AtomicLong atomicLong = new AtomicLong(0);
        for (int i = 0; i < 8 ; i++) {
            threadPoolExecutor.submit(new Runnable() {
                @Override
                public void run() {
                    for (int j = 0; j <1000 ; j++) {

                        //加1返回旧值
                        System.out.println(atomicLong.getAndIncrement());
                        //加1返回新值
                        System.out.println(atomicLong.incrementAndGet());

                        //减1返回旧值
                        System.out.println(atomicLong.getAndDecrement());
                        //减1返回新值
                        System.out.println(atomicLong.decrementAndGet());
                    }
                }
            });

        }

    }
}
~~~

######getAndIncrement()
原子加1，返回旧值

######incrementAndGet()
原子加1返回新值

######getAndDecrement
原子减1，返回旧值
######decrementAndGet
原子减1，返回新值



###
在java8中提供了updateAndGet和accumulateAndGet方法

atomicLong,updateAndGet(x -> Max.max(x, observed));

atomicLong.accumulateAndGet(observed, Math::max);

同时也提供了返回原始值的对应方法：getAndUpdate、getAndAccumulate
