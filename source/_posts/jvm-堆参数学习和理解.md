---
title: jvm-堆参数学习和理解.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
---
title: jvm-堆参数学习和理解.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: jvm
categories: jvm
---
>三人行，必有我师

###堆区内存配置参数
######-Xms
 s可以理解start开始，设置堆的初始分配大小；默认为物理内存的 1/64
######-Xmx
 x可以理解为max最大，设置最大分配内存，默认为物理内存的 1/4

>开发过程中，通常会将-Xms 与-Xmx两个参数的配置相同的值，其目的是为了能够在java垃圾回收机制清理完堆区后不需要重新分隔计算堆区的大小而浪费资源。

===================新生代================================
######-XX:NewSize
设置堆中新生代大小
######-XX:MaxNewSize
设置新生代最大内存大小
######-Xmn 
同时设置NewSize与MaxNewSize，将之设置为一致大小
可以这样理解==> -XX:newSize = -XX:MaxnewSize　=　-Xmn
 默认是物理内存的1/64
===================================================

 ######-XX:SurvivorRatio
设置新生代中`Eden区`与`Survivor区`的大小比值。

SurvivorRatio的默认值为8，意思就是Edon和Survivor1、Survivor2 的比例默认是8：1：1


######-XX:NewRatio
 设置`年老代`(除去持久代) 与 `新生代`(包括Eden和两个Survivor区)的比值；默认为2 ，则老年代和新生代的比是  2:1

==================永久区=================================
######-XX:PermSize 
设置持久代/永久区初始值，默认为物理内存的1/64
######-XX:MaxPermSize 
设置持久代/永久区最大值，默认为物理内存的1/4

===================================================

######-XX:MaxTenuringThreshold
 设置垃圾最大年龄。默认15（对象被复制的次数）

- 如果设置为0的话,则年轻代对象不经过Survivor区,直接进入年老代。 对于年老代比较多的应用，可以提高效率。

- 如果将此值设置为一个较大值，就能防止大量对象进入老年区。则新生代对象会在Survivor区进行多次复制，这样可以增加对象在新生代的存活时间，增加在年轻代即被回收的概率。 



    
###关于jvm内存的计算问题
1、对于JVM内存配置参数：
-Xmx10240m -Xms10240m -Xmn5120m -XXSurvivorRatio=3
,其最小内存值和Survivor区总大小分别是多少？

①、从-Xmx10240m -Xms10240m可以得出 堆大小为 10240
②、-Xmn5120m可以得出 新生代大小为 5120 
③、  -XXSurvivorRatio=3 可以得出 伊甸区：幸存者1：幸存者2 比值为 3:1:1
④、可以得出幸存者区总大小  5120 * 2/5 = 2048






###其它配置
######-Xss128k
设置每个线程的堆栈大小为128k。JDK5.0以后每个线程堆栈大小为1M，以前每个线程堆栈大小为256K。更具应用的线程所需内存大小进行调整。在相同物理内存下，减小这个值能生成更多的线程。但是操作系统对一个进程内的线程数还是有限制的，不能无限生成，经验值在3000~5000左右。线程栈的大小是个双刃剑，如果设置过小，可能会出现`栈溢出`，特别是在该线程内有递归、大的循环时出现溢出的可能性更大，如果该值设置过大，就有影响到`创建栈的数量`，如果是多线程的应用，就会出现内存溢出的错误．

######生成堆内存快照
~~~
java -Xmx10m -Xms10m -XX:+HeapDumpOnOutOfMemoryError -jar identityauthsrv-2.2.18-base-alpha.jar
~~~
生成了快照文件
![image.png](https://upload-images.jianshu.io/upload_images/13965490-739b12a22d9fbacc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> -XX:+HeapDumpOnOutOfMemoryError


######查看当前jvm中 Xms  和 Xmx 的内存大小
~~~
    public static void main(String[] args) {
        long totalMemory = Runtime.getRuntime().totalMemory(); //JVM中的初始内存总量
        long maxMemory = Runtime.getRuntime().maxMemory(); //JVM试图使用的最大内存
        System.out.println("totalMemory = " + totalMemory + "Byte 、 " +(totalMemory / (double) 1024 )+   "Kb 、 " +(totalMemory / (double) 1024 / 1024) + " MB");
        System.out.println("MaxMemory = " + maxMemory + " Byte 、 " +(totalMemory / (double) 1024 )+   "Kb 、 "+ (maxMemory / (double) 1024 / 1024) + " MB");
    }
~~~





