---
title: jvm-监控命令工具之-jstat.md
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
title: jvm-监控命令工具之-jstat.md
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
**JVM Statistics Monitoring Tool**

**命令行中运行期间定位虚拟机性能问题首选工具,常用于检查垃圾回收以及内存泄漏问题**

*   **格式: `jstat -<option> [-t] [-h] <vmid> [interval] [count]`**
    *   option: 要查看什么统计信息
    *   -t : 程序运行到现在耗时
    *   -h : 输出多少行后输出一次表头信息
    *   vmid: 要查看的进程号
    *   interval: 间隔多少毫秒输出一次统计信息
    *   count: 输出多少次终止


>jstat -class -t -h5 10704 2000 10
Timestamp       Loaded  Bytes  Unloaded  Bytes     Time
        23791.8   4131  7525.3      210   216.0       3.71
        23793.9   4131  7525.3      210   216.0       3.71
        23795.9   4131  7525.3      210   216.0       3.71
        23814.6   4131  7525.3      210   216.0       3.71
        23816.6   4131  7525.3      210   216.0       3.71
Timestamp       Loaded  Bytes  Unloaded  Bytes     Time
        23818.7   4131  7525.3      210   216.0       3.71
        23820.7   4131  7525.3      210   216.0       3.71
        23822.6   4131  7525.3      210   216.0       3.71
        23824.7   4131  7525.3      210   216.0       3.71
        23826.7   4131  7525.3      210   216.0       3.71

![image-20210517215059917](https://upload-images.jianshu.io/upload_images/13965490-de4a606a04495104.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### option的种类

选项option可以由以下值构成
####类装载相关的:
1、-class:显示ClassLoader的相关信息:类的装载、卸载数量、总空间、类装载所消耗的时间等
垃圾回收相关的:
2、-gc:显示与GC相关的堆信息。包括Eden区、两个Survivor区、老年代、永久代等的容量、已用空间、GC时间合计等信息。
3、-gccapacity:显示内容与-gc基本相同，但输出主要关注Java堆各个区垃使用到的最大、最小空间。
4、-gcutil:显示内容与-gc基本相同，但输出主要关注已使用空间占总空间的百分比。
5、-gccause:与-gcutil功能一样，但是会额外输出导致最后一次或当前正在发生的Gc产生的原因。
6、-gcnew:显示新生代GC状况
7、-gcnewcapacity:显示内容与-gcnew基本相同，输出主要关注使用到的最大、最小空间
8、-geold:显示老年代GC状况
9、-gcoldcapacity:显示内容写-gco1d基本相同，输出主要关注使用到的最大、最小空间
10、-gcpermcapacity:显示永久代使用到的最大、最小空间。
####JIT相关的:
11、-compiler:显示JIT编译器编译过的方法、耗时等信息.
12、-printcompilation:输出已经被JIT编译的方法


###-gc 参数说明

####新生代相关
S0C是第—个幸存者区的大小(字节)
S1C是第二个幸存者区的大小(字节)
S0U是第—个幸存者区已使用的大小（字节)
S1U是第二个幸存者区已使用的大小(字节)
EC是Eden空间的大小（字节)
EU是Eden空间已使用大小（字节)

####老年代相关
OC是老年代的大小(字节)
OU是老年代已使用的大小（字节)

####方法区（元空间)相关
MC是方法区的大小
MU是方法区已使用的大小
CCSC是压缩类空间的大小
CCSU是压缩类空间已使用的大小
####其他
YGC是从应用程序启动到采样时young gc的次数
YGCT是指从应用程序启动到采样时young gc消耗时间(秒)
FGC是从应用程序启动到采样时full gc的次数
FGCT是从应用程序启动到采样时的full gc的消耗时间（秒)
GCT是从应用程序启动到采样时gc的总时间


### 重点经验

*   **当GC时间占总时间比率很大时,说明频繁GC,越大越可能OOM**

    *   计算GC占比公式 = 2次GC耗时时间相减 / 这2次程序持续时间相减

        ![image-20210517225915759](https://upload-images.jianshu.io/upload_images/13965490-f5fb30205f08781b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

*   **当老年代占用内存不断上涨,可能出现内存泄漏**

    [图片上传失败...(image-2a4d27-1644219396353)]
