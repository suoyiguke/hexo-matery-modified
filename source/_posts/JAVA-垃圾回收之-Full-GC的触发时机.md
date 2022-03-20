---
title: JAVA-垃圾回收之-Full-GC的触发时机.md
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
title: JAVA-垃圾回收之-Full-GC的触发时机.md
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
活下来的年轻代对象被复制到老年代 。 老年代的内存区域一般大于年轻代 。 因为它拥有更大的规模，为了提高系统整体性能，所以 GC 发生的次数比在年轻代的少。对象从老年代消失时，我们说“M句orGC”或“ Full GC ＂发生了


###自动触发Full GC的情况有下面5种
除了直接调用 System.gc 外，触发 Full GC 执行的情况有如下四种。

######1、老年代空间不足
老年代空间只有在年轻代对象转入及创建为大对象、大数组时才会出现不足的现象，当执行 Full GC 后空间仍然不足，则抛出如下错误 Java.lang.OutOfMemoryError: Java heap space 。
为了避免以上两种状况引起的 Full GC，调优时应尽量做到让对象在 MinorGC 阶段被回收，让对象在年轻代多存活一段时间，以及尽量不要创建过大的对象及数组。


######2、永久代空间满
永久代中存放的是一些类的信息，当系统中要加载的类、反射的类和调用的方法较多时，永久代可能会被占满，在未配置为采用 CMSGC 的情况下会执行 Full GC。
如果经过 Full GC 仍然回收不了，那么 JVM 会抛出如下错误信息java.lang.OutOfMemoryError: PerrnGen space 。
为了避免永久代被占满造成 Full GC 现象，可采用的方法为增大永久代空间或转为使用CMSGC 。
`当然，在JDK6时永久代GC是被 Full GC所管理的`


######3、CMS GC 时出现 Promotion Failed 和 Concurrent Mode Failure
对于采用 CMS 进行老年代 GC 的程序而言，尤其要注意 GC 日志中是否有 Promotion Failed和 Concurrent Mode Failure 两种状况，当这两种状况出现时可能会触发 Full GC 。

> `Promotion Failed` 是在进行 MinorGC 时， Survivor Space 放不下、对象只能放入老年代，而此时老年代也放不下时造成的  。 

>`Concurrent Mode Failure` 是在执行 CMS GC 的过程中，同时有对象要放入老年代，而此时老年代空间不足造成的 。

>应对措施为增大 Survivor Space、老年代空间或调低触发并发 GC 的比率，但在 JDK5.0＋、6.0＋的版本中有可能会由于 JDK 的 Bug29 导致 CMS 在 Remark 完毕后很久才触发清除动作。对于这种状况，可通过设置选项－XX:CMSMaxAbortablePrecleanTime=5 （单位为毫秒〉来避免。


######4、 统计得到的 MinorGC 晋升到老年代的平均大小大于老年代的剩余空间
>这是一个较为复杂的触发情况， HotSpot 为了避免由于年轻代对象晋升到老年代导致老年代空间不足的现象，在进行 MinorGC 时，做了一个判断，如果之前统计所得到的 MinorGC 晋升到老年代的平均大小大于老年代的剩余空间，那么就直接触发 Full GC 。
例如程序第一次触发 MinorGC 后，有仙IB 的对象晋升到老年代，那么当下一次 Minor GC发生时，首先检查老年代的剩余空间是否大于 6MB，如果小于 6MB ，则执行 Full GC。当年轻代采用 Parallel GC 时， 方式稍有不同 ， Parallel GC 是在 Minor GC 后也会检查，例如上面的例子中第一次 MinorGC 后， GC 会检查此时老年代的剩余空间是否大于 6MB，如小于，则触发对老年代的回收。



######5、除了以上 4 种状况外，对于使用 RMI 来进行 RPC 或管理的 Sun JDK 应用而言 ，默认情况下会 一小时执行一次 Full GC ，这个执行间 隔时间是可以配置的。

>允许在启动时通过 
－Java-Dsun.rmi.dgc.client.gclnterval = 3600000 来设置 Full GC 执行的间隔时间或通过
－XX : +DisableExplicitGC 来禁止 RMI 调用 System .gc 。
