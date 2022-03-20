---
title: jvm-监控GUI工具之-Profile-熟练.md
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
title: jvm-监控GUI工具之-Profile-熟练.md
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
Profile 熟练

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E7%AE%80%E4%BB%8B)简介

![image-20210520231804931](https://upload-images.jianshu.io/upload_images/13965490-a02bda4f1c395375.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image-20210520231834027](https://upload-images.jianshu.io/upload_images/13965490-6d31f024321f5f17.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E6%95%B0%E6%8D%AE%E9%87%87%E9%9B%86%E6%96%B9%E5%BC%8F)数据采集方式

*   instrumentation 重构模式
    *   堆栈信息准确,对性能有影响
*   sampling 样本采集 (推荐使用)
    *   样本统计(默认5ms)统计信息,性能影响小

![image-20210520235805487](https://upload-images.jianshu.io/upload_images/13965490-c9d99a10e72402b9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E6%91%87%E6%9D%86%E6%A3%80%E6%B5%8B-telemetries)摇杆检测 Telemetries

![image-20210521093956938](https://upload-images.jianshu.io/upload_images/13965490-217239eee0bc72cb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E5%86%85%E5%AD%98%E8%A7%86%E5%9B%BE%E5%88%86%E6%9E%90-live-memory)内存视图分析 Live memory

可以通过对比分析,如果增加很多对象可能有几种情况

1.  **频繁创建对象,死循环或循环次数多**
2.  **存在大对象(读取文件byte[]不要太大,边写边读,长时间不写出会导致byte[]过大)**
3.  **每次GC后,内存依次递增可能存在内存泄漏**

![image-20210521145844721](https://upload-images.jianshu.io/upload_images/13965490-5e18bd5ae67068b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

*   All Objects 所有对象
    *   Size显示的是该实例对象的浅堆(不包含它引用字段的实际大小)
*   Recorded Objects 记录对象
    *   可以动态看到类的对象变化情况 (默认不开启,开启后影响性能)

![image-20210521145941114](https://upload-images.jianshu.io/upload_images/13965490-4c77ad0d221c7fba.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

*   Allocation Call Tree 分配访问树
    *   将执行方法所占时间显示成树 (默认不开启,开启后影响性能)

![image-20210521150407870](https://upload-images.jianshu.io/upload_images/13965490-993429caf14fd6fb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

*   Allocation Call Tree 分配热点
    *   显示什么方法时间占比大

![image-20210521150855253](https://upload-images.jianshu.io/upload_images/13965490-4554c1df971d7a16.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

*   Class Tracker 类追踪器

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E5%A0%86%E9%81%8D%E5%8E%86-heap-walker)堆遍历 Heap Walker

通过对比发现对象增长过快,可以查看该对象的引用链

![image-20210521153855310](https://upload-images.jianshu.io/upload_images/13965490-38653dca0f9fe8d4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image-20210521154115936](https://upload-images.jianshu.io/upload_images/13965490-9c7a8630833c9d03.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image-20210521154221915](https://upload-images.jianshu.io/upload_images/13965490-927985adf08b1b04.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#cpu-%E8%A7%86%E5%9B%BE-cpu-views)CPU 视图 CPU views

![image-20210521154659902](https://upload-images.jianshu.io/upload_images/13965490-93d5d1681e7e7b72.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

关于这种分析 都可以从范围大的到范围小的 **package -> class -> method**

![image-20210521154546655](https://upload-images.jianshu.io/upload_images/13965490-1004c303eb858750.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E7%BA%BF%E7%A8%8B%E8%A7%86%E5%9B%BE-threads)线程视图 Threads

![image-20210521154933931](https://upload-images.jianshu.io/upload_images/13965490-0ef9ae324b90660c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

查看线程运行状态,可以知道线程执行情况,比如main线程大部分时间在等待,少部分时间在运行

![image-20210521154809697](https://upload-images.jianshu.io/upload_images/13965490-175a6d3560a3b370.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E7%9B%91%E8%A7%86%E5%99%A8%E5%92%8C%E9%94%81-monitors--locks)监视器和锁 Monitors & Locks

![image-20210521155003657](https://upload-images.jianshu.io/upload_images/13965490-1d718c8a5d30379b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
