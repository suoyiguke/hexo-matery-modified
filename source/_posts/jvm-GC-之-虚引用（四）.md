---
title: jvm-GC-之-虚引用（四）.md
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
title: jvm-GC-之-虚引用（四）.md
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
> 一辈子要跟自己的无知做斗争 

弱引用也称为“幽灵引用”或者“幻影引用”， 它是最弱的一种引用关系。 一个对象是否有虚引用的存在， 完全不会对其生存时间构成影响， 也无法通过虚引用来取得一个对象实例。 为一个对象设置虚引用关联的唯一目的只是为了能在这个对象被收集器回收时收到一个系统通知。 在JDK 1.2版之后提供了PhantomReference类来实现虚引用。

这个虚引用比较特殊，不同于之前讲的强、软、弱引用。来看下PhantomReference的构造器
![image.png](https://upload-images.jianshu.io/upload_images/13965490-7ce7d1c1cf3652d3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
似乎需要一个java.lang.ref.ReferenceQueue类来作为参数才能构造。从名字可以看出它是一个队列了。

我们再来看看PhantomReference的 get方法源码
![image.png](https://upload-images.jianshu.io/upload_images/13965490-63bd1b8880f74d1e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

对，你没有看做。这个get方法始终返回null，哪它有什么用？存心来找茬的？
jdk中既然有这个类，肯定有它存在的道理。


> 虚引用必须与ReferenceQueue一起使用，当GC准备回收一个对象，如果发现它还有虚引用，就会在回收之前，把这个虚引用加入到与之关联的ReferenceQueue中。

换句话说，虚引用回收之后，ReferenceQueue队列中会存在虚引用对象的实例
