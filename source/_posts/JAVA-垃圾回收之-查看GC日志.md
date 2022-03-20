---
title: JAVA-垃圾回收之-查看GC日志.md
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
title: JAVA-垃圾回收之-查看GC日志.md
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
>慢慢尝试着放缓说话的速度，留给自己思考时间的同时也能让对方听的f清楚
###复杂日志
在idea中配置
~~~
-Xms1024m -Xmx1024m -XX:+PrintGCDetails
~~~
![image.png](https://upload-images.jianshu.io/upload_images/13965490-731cf613816a9c25.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###从打印的堆内存结构可以看出一些信息
![image.png](https://upload-images.jianshu.io/upload_images/13965490-81e60c6b900d0fdd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- PSYoungGen（新生代）+ParOldGen（老年代） = MaxMemory（JVM堆内存初始值/最大值）
305664K+699392K = 1005056.0K

- Metaspace(元空间) 是概念上的，物理上其实不存在

- PSYoungGen（新生代）又分为
     1、eden 伊甸园区
     2、from 幸存者1区
     3、to  幸存者2区
![image.png](https://upload-images.jianshu.io/upload_images/13965490-a472962fd7c2bde0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###举个例子
这行GC日志所表达的信息的意思？

[GC (Allocation Failure) [PSYoungGen: 2048K->504K(2560K)] 2048K->1091K(9728K), 0.0041828 secs] [Times: user=0.00 sys=0.00, real=0.00 secs] 

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7d075bf83d6787dc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


发生在新年轻代的GC: GC前年轻代占用2048K，GC后年轻代占用504K,年轻代总共2560K；GC前JVM堆内存占用2048K，GC后JVM堆内存占用1091K，JVM堆内存一共9728K

- 我设置的JVM堆内存是10M，而GC日志显示只有9728K

###简单日志
可以使用 这个参数 -verbose:gc
