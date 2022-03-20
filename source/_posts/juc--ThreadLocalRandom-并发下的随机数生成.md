---
title: juc--ThreadLocalRandom-并发下的随机数生成.md
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
title: juc--ThreadLocalRandom-并发下的随机数生成.md
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
> 误在沙地筑高楼

我们知道虽然java.util.Random是线程安全的，但是它在多线程访问同一个实例时，性能表现非常糟糕。jdk1.7提供了java.util.concurrent.ThreadLocalRandom 类，企图将它和Random结合以克服所有的性能问题，该类继承自Random。


######ThreadLocalRandom使用方法
它的构造器是私有的，如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-fa54771b7f6ddd91.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

因此不能自己创建ThreadLocalRandom实例，可以使用它的静态工厂 ThreadLocalRandom.current()


######ThreadLocalRandom确定单例的

运行下列程序，可得打印的hashcode相同。说明ThreadLocalRandom.current()得到的对象是单实例的
~~~
package io.renren;
import java.util.Random;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ThreadLocalRandom;

public class Test_Random {


    public static void main(String[] args) {

        for (int i = 0; i < 3; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    System.out.println( ThreadLocalRandom.current().hashCode());
                }
            }).start();
        }

    }
}
~~~

但是既然名字里有ThreadLocal的字眼，那么和线程绑定的变量是谁呢？ 原来ThreadLocalRandom在jdk1.7的实现是直接使用到了ThreadLocal，让ThreadLocalRandom有多个实例，每个实例绑定到特定线程上。但是jdk1.8已经不是用ThreadLocal来实现了，只是借鉴了它的思想。

ThreadLocalRandom使用ThreadLocal的原理，让每个线程内持有一个本地的种子变量，该种子变量只有在使用随机数时候才会被初始化，多线程下计算新种子时候是根据自己线程内维护的种子变量进行更新，从而避免了竞争。

######ThreadLocalRandom使用注意
所以在多线程下使用ThreadLocalRandom，必须调用一次current方法未为当前线程生成一个新种子，如果只调用一次current方法，那么最终生成的随机数会相同。这是一种错误的用法。如下

~~~
package io.renren;
import java.util.concurrent.ThreadLocalRandom;
public class Test_Random {
    public static void main(String[] args) {
        ThreadLocalRandom current = ThreadLocalRandom.current();
        for (int i = 0; i < 3; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    System.out.println( current.hashCode());
                }
            }).start();
        }
    }
}
~~~
结果
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d33ab1c6691f9d9e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
