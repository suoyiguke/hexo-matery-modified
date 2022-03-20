---
title: JAVA-垃圾回收之-弱引用（四）.md
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
title: JAVA-垃圾回收之-弱引用（四）.md
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
> 学不可以已

弱引用也是用来描述那些非必须对象， 但是它的强度比软引用更弱一些，软引用需要等到jvm堆内存实在不够了才会被回收。` 而被弱引用关联的对象只能生存到下一次垃圾收集发生为止。` 当垃圾收集器开始工作， 无论当前内存是否足够， 都会回收掉只被弱引用关联的对象。 在JDK 1.2版之后提供了WeakReference类来实现弱引用。

> 弱引用的特点是不管内存是否足够，只要发生GC，都会被回收

######怎么创建一个弱引用对象呢？

>WeakReference<Test> weakReference= new WeakReference<>(new Test());

同样，它也提供了get方法；返回它包装的弱引用对象。若此对象已经被GC回收，则此方法返回null 。 



######探究弱引用的回收时机


如下列程序：

~~~
package io.renren;
import java.lang.ref.WeakReference;
import java.util.concurrent.TimeUnit;
/**
 * @author: yinkai
 * @create: 2020-03-20 10:53
 */
class Test {
    static WeakReference<Test> weakReference = new WeakReference<>(new Test());
    /**
     * 重写Object类的finalize方法
     */
    @Override
    protected void finalize() {
        System.out.println(System.currentTimeMillis() + " Test 被回收了");
        //回收后打印！
        System.out.println(weakReference.get());
    }
    public static void main(String[] args) {
        System.out.println("GC之前 " + System.currentTimeMillis() + weakReference.get());
        System.gc();
        System.out.println("GC之后 " + System.currentTimeMillis() + weakReference.get());
        //等待GC线程执行垃圾回收
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
~~~
执行上列程序
![image.png](https://upload-images.jianshu.io/upload_images/13965490-121165fee5eaa924.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



可以很清楚的看到明明内存还很充足，但是手动调用 System.gc(); 触发了GC，test对象还是被回收了。


######如果弱引用指向的对象上还有强引用
我们再来看下面的例子，new Test("test1")对象被test1变量强引用，又被weakReference弱引用。那么即使触发GC，该对象也不会被回收，因为还存在强引用。

~~~
package io.renren;
import java.lang.ref.WeakReference;
import java.util.concurrent.TimeUnit;
/**
 * @author: yinkai
 * @create: 2020-03-20 10:53
 */
class Test {
    private String name;

    public Test(String name) {
        this.name = name;
    }
    public Test(){}
    /**
     * 重写Object类的finalize方法
     */
    @Override
    protected void finalize() {
        System.out.println(System.currentTimeMillis() +" " + name +" 被回收了");
    }
    public static void main(String[] args) {
        //test1 强引用
        Test test1 = new Test("test1");
        WeakReference<Test> weakReference = new WeakReference<>(test1);
        // test1 = null;
        System.out.println("GC之前 " + System.currentTimeMillis() + weakReference.get());
        System.gc();
        System.out.println("GC之后 " + System.currentTimeMillis() + weakReference.get());
        //等待GC线程执行垃圾回收
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-96541802afcdc20a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

如果将// test1 = null;的注释去掉，再执行。这样的结果将和上面的结果有很大区别，如下
![image.png](https://upload-images.jianshu.io/upload_images/13965490-26cd97a788c9c3c3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
说明new Test("test1")对象被回收了，因为强引用被GC Roots识别为`不可达`

> 如此可见，一个对象是否被回收，是要看它上面的所有引用。而不是单单那么显眼的一个


######弱引用的应用
 弱引用在很多地方都有用到，比如java.lang.ThreadLocal、java.util.WeakHashMap。
