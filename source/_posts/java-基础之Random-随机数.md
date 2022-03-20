---
title: java-基础之Random-随机数.md
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
> 吾生也有涯，而知也无涯

######使用Random 生成指定大小范围内的随机数

> 公式:  random.nextInt(n -m + 1) +m;

如下生成[22,433]范围内的随机数，注意两边都是闭区间。22和443都会取得到
~~~
package io.renren;
import java.util.Random;
public class RandomTest {

    public static void main(String[] args) {
        Random random = new Random(1);
        // [22,433]
        for (int i = 0; i <1000 ; i++) {
            System.out.println(random.nextInt(433-22+1) + 22);
        }
    }

}
~~~

######Random 是线程安全的么？可以被线程共享一个实例么？
在工程中不同地方生成随机数总是new了很多个Random 实例，想着这个Random 能不能复用。于是打开jdk文档看看，里面有提到

>java.util.Random的是线程安全的。 但是，跨线程的同时使用java.util.Random实例可能会遇到争用，从而导致性能下降。 在多线程设计中考虑使用[`ThreadLocalRandom`](../../java/util/concurrent/ThreadLocalRandom.html "java.util.concurrent中的类") 。

文档中说明了Random是线程安全的，但是不建议多线程访问同一个实例。因为会带来效率问题。我们来看看Random的源码探究下

nextInt方法里调用了next方法
![image.png](https://upload-images.jianshu.io/upload_images/13965490-d2b9900682d44567.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

那么再看看next方法，可以看到next方法里为了保证seed对象是最新的就调用了compareAndSet方法

![image.png](https://upload-images.jianshu.io/upload_images/13965490-661203cd1e2d7be2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
我们知道compareAndSet是著名的`CAS` 乐观锁算法，而这种算法在激烈的并发修改下会导致自旋次数过多。从而长时间占用cpu执行时间片。

那么这种建议背后的原理就一目了然了。而且在《阿里巴巴Java开发手册》中也有提到：
>【推荐】 避免 Random 实例被多线程使用，虽然共享该实例是线程安全的，但会因竞争同一seed 导致的性能下降。
说明：Random 实例包括 java.util.Random 的实例或者 Math.random()的方式。
正例：在 JDK7 之后，可以直接使用 API ThreadLocalRandom，而在 JDK7 之前，需要编码保证每个线程持有一个实例

JDK7之前可以使用ThreadLocal为每一个线程绑定一个Random 实例。JDK7之后就有一个现成的ThreadLocalRandom类可以使用了


######ThreadLocalRandom 多线程共享随机数生成
关于ThreadLocalRandom 可以看看这篇文章
https://www.jianshu.com/p/bf276d506668
