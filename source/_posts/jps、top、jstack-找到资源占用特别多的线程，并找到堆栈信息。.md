---
title: jps、top、jstack-找到资源占用特别多的线程，并找到堆栈信息。.md
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
title: jps、top、jstack-找到资源占用特别多的线程，并找到堆栈信息。.md
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

1、使用jps，找到对应程序的pid（第一列）
~~~
root@7489c31b97ee:/# jps
1 app.jar
840 Jps
~~~

2、使用top -Hp 进程pid 
打印该进程下面的所有线程占用资源排名，找到第一名的pid=702
~~~
 references: 2830

root@7489c31b97ee:/# top -Hp 1
top - 08:30:45 up 33 days,  6:36,  0 users,  load average: 0.22, 0.49, 0.69
Threads:  89 total,   0 running,  89 sleeping,   0 stopped,   0 zombie
%Cpu(s):  1.5 us,  2.2 sy,  0.0 ni, 96.3 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem:  30715748 total, 14211524 used, 16504224 free,        0 buffers
KiB Swap: 10289148 total,  9820864 used,   468284 free.  1575056 cached Mem

  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND                                                                                                                           
  702 root      20   0 7994356 1.153g  14192 S  2.3  3.9   0:13.68 java                                                                                                                              
  699 root      20   0 7994356 1.153g  14192 S  2.0  3.9   0:13.88 java                                                                                                                              
    1 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.01 java                                                                                                                              
    8 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:24.91 java                                                                                                                              
    9 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.35 java                                                                                                                              
   10 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.34 java                                                                                                                              
   11 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.32 java                                                                                                                              
   12 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.31 java                                                                                                                              
   13 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.31 java                                                                                                                              
   14 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.34 java                                                                                                                              
   15 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.28 java                                                                                                                              
   16 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.38 java                                                                                                                              
   17 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.87 java                                                                                                                              
   18 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.10 java                                                                                                                              
   19 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.14 java                                                                                                                              
   20 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.00 java                                                                                                                              
   21 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:25.87 java                                                                                                                              
   22 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:24.75 java                                                                                                                              
   23 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:25.63 java                                                                                                                              
   24 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:08.06 java                                                                                                                              
   25 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.03 java                                                                                                                              
   26 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.36 java                                                                                                                              
  698 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.03 java                                                                                                                              
  700 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.06 java                                                                                                                              
  701 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.01 java                                                                                                                              
  703 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.11 java                                                                                                                              
  706 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.06 java                                                                                                                              
  707 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.07 java                                                                                                                              
  708 root      20   0 7994356 1.153g  14192 S  0.0  3.9   0:00.00 java                                                                                                                              
root@7489c31b97ee:/# 

~~~

3、jstack 进程pid，查看最高占用资源的进程堆栈信息
~~~~
root@7489c31b97ee:/# jstack 1
2022-01-19 08:37:58
Full thread dump OpenJDK 64-Bit Server VM (25.111-b14 mixed mode):

"NFLoadBalancer-PingTimer-service-rbac" #773 daemon prio=5 os_prio=0 tid=0x00007f0b98031800 nid=0x346 in Object.wait() [0x00007f0b8e8f9000]
   java.lang.Thread.State: TIMED_WAITING (on object monitor)
	at java.lang.Object.wait(Native Method)
	at java.util.TimerThread.mainLoop(Timer.java:552)
	- locked <0x00000000fb3fdd58> (a java.util.TaskQueue)
	at java.util.TimerThread.run(Timer.java:505)

"RibbonApacheHttpClientConfiguration.connectionManagerTimer" #772 daemon prio=5 os_prio=0 tid=0x00007f0b98077000 nid=0x345 in Object.wait() [0x00007f0b8e9fa000]
   java.lang.Thread.State: TIMED_WAITING (on object monitor)
	at java.lang.Object.wait(Native Method)
	at java.util.TimerThread.mainLoop(Timer.java:552)
	- locked <0x00000000fb4c2e20> (a java.util.TaskQueue)
	at java.util.TimerThread.run(Timer.java:505)
~~~

jstack命令生成的thread dump信息包含了JVM中所有存活的线程，为了分析指定线程，必须找出对应线程的调用栈，应该如何找？

在top命令中，已经获取到了占用cpu资源较高的线程pid，将该pid转成16进制的值，在thread dump中每个线程都有一个nid，找到对应的nid即可；隔段时间再执行一次stack命令获取thread dump，区分两份dump是否有差别，在nid=0x246c的线程调用栈中，发现该线程一直在执行JstackCase类第33行的calculate方法，得到这个信息，就可以检查对应的代码是否有问题。

线程pid=702 ==> 转16进制为 2be。那么对应的堆栈信息如下：

![image.png](https://upload-images.jianshu.io/upload_images/13965490-0dcca6f59382b1fc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这块的业务代码是分布式事务框架seata相关的：
io.seata.core.rpc.netty.AbstractNettyRemotingClient.MergedSendRunnable
![image.png](https://upload-images.jianshu.io/upload_images/13965490-dc2000cab394d064.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




###比较后的方法
（3）把线程号转换为16进制
~~~
[root@localhost ~]# printf "%x" 7287
1c77
~~~
记下这个16进制的数字，下面我们要用

（4）用jstack工具查看线程栈情况
~~~
[root@localhost ~]# jstack 7268 | grep 1c77 -A 10
"http-nio-8080-exec-2" #16 daemon prio=5 os_prio=0 tid=0x00007fb66ce81000 nid=0x1c77 runnable [0x00007fb639ab9000]
   java.lang.Thread.State: RUNNABLE
 at com.spareyaya.jvm.service.EndlessLoopService.service(EndlessLoopService.java:19)
 at com.spareyaya.jvm.controller.JVMController.endlessLoop(JVMController.java:30)
 at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
 at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
 at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
 at java.lang.reflect.Method.invoke(Method.java:498)
 at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:190)
 at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:138)
 at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:105)
~~~
通过jstack工具输出现在的线程栈，再通过grep命令结合上一步拿到的线程16进制的id定位到这个线程的运行情况，其中jstack后面的7268是第（1）步定位到的进程号，grep后面的是（2）、（3）步定位到的线程号。

从输出结果可以看到这个线程处于运行状态，在执行com.spareyaya.jvm.service.EndlessLoopService.service这个方法，代码行号是19行，这样就可以去到代码的19行，找到其所在的代码块，看看是不是处于循环中，这样就定位到了问题。
