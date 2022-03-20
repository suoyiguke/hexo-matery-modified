---
title: JAVA-垃圾回收之-软引用（三）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: JAVA-GC
categories: JAVA-GC
---
---
title: JAVA-垃圾回收之-软引用（三）.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: JAVA-GC
categories: JAVA-GC
---
>锲而不舍，金石可镂

软引用是用来描述一些还有用， 但非必须的对象。 只被软引用关联着的对象。
在系统将要发生内存溢出异常前， 会把这些对象列进回收范围之中进行第二次回收， 如果这次回收还没有足够的内存，才会抛出内存溢出异常。 在JDK 1.2版之后提供了SoftReference类来实现软引用。

> 软引用的特点是在程序需要申请一个较大内存区域而堆中已无能容下它的空闲内存时。此时可能出现OOM，那么所有软引用对象均会被GC回收

######怎么创建一个软引用对象呢？
使用SoftReference将目标对象保包装即可，这样的test对象就是软引用的
>SoftReference<Test> softReference = new SoftReference<>(new Test());

可以看看它的get方法
> get() 返回此引用对象。 如果对象已GC回收，则此方法返回 null 。




######我们来看看软引用对象的回收时机

先将jvm参数设为下列，表示将以20M的堆内存运行程序
>-Xms20M -Xmx20M


如下列程序： 
> Test 类里面定义了一个字节数组实例属性`bytes` ，将占用内存10M
> 在执行System.gc();之后再次申请一个字节数组，也占用内存10M
~~~
package io.renren;

import java.lang.ref.SoftReference;

/**
 * @author: yinkai
 * @create: 2020-03-20 10:53
 */
class Test {

    //bytes占用堆内存10M
    byte[] bytes = new byte[1024 * 1024 * 10];

    static SoftReference<Test> softReference = new SoftReference<>(new Test());

    /**
     * 重写Object类的finalize方法
     */
    @Override
    protected void finalize() {
        System.out.println(System.currentTimeMillis() + " Test 被回收了");
        //回收后打印软引用的test对象！
        System.out.println(softReference.get());
    }


    //堆内存总共20M
    public static void main(String[] args) {
       
        System.out.println("GC之前 " + System.currentTimeMillis() + softReference.get());
        System.gc();
        System.out.println("GC之后 " + System.currentTimeMillis() + softReference.get());

        //再次申请一个占用10M的对象,此时内存不够了，软引用对象会被回收！
        byte[] bytes = new byte[1024 * 1024 * 10];


    }
}
~~~

执行上面程序 
![image.png](https://upload-images.jianshu.io/upload_images/13965490-443ed2ae7e7ab514.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以很清楚的看到手动完成GC后，SoftReference 包裹的test对象未被回收；
之后我们又要申请一个10M的字节数组，最大堆内存不够了，所以把软引用对象包裹的byte[]给干掉了，在上诉例子中即使将test对象回收掉，剩下的空闲堆内存仍然不够分配10M，所以还是抛出了OOM。

将新申请的字节数组设为1024 * 1024 * 1的大小：`byte[] bytes = new byte[1024 * 1024 * 1];  ` 重新运行程序
![image.png](https://upload-images.jianshu.io/upload_images/13965490-475d7e1ecb5ebe73.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
此时软引用对象未被GC回收

>所以可以得出结论：在虚拟机抛出`OutOfMemoryError`之前，软引用对象可以被GC回收。但剩余堆内存空间足够容纳新申请的对象，那么软引用指向对象不会被GC回收。

######是不是所有的软引用都会被GC回收？
我们知道在jvm堆内存空间的不够的情况下会去回收软引用指向的对象，但是是不是所有的软引用对象都会被GC回收掉？
事实上，JVM是很聪明的，会尽可能优先回收长时间闲置不用的软引用指向的对象，对那些刚构建的或刚使用过的软引用指向的对象尽可能的保留。



######软引用在开发中的应用


此类的直接实例可用于实现简单的缓存; 此类或派生子类也可用于较大的数据结构以实现更复杂的高速缓存。
当内存足够，可以正常的拿到缓存，当内存不够，就会先干掉缓存，不至于马上抛出OOM。
