---
title: jvm-监控GUI工具之-eclipse插件MAT.md
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
title: jvm-监控GUI工具之-eclipse插件MAT.md
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
###目的
  当运行java程序发生OOM时，可以通过内存分析工具MAT进行问题跟踪，并解决

  MAT是eclipse的插件，针对idea，在本机安装独立版使用

###安装

  下载地址：https://eclipse.org/mat/downloads.php

  找到对应版本下载

　 解压得到mat文件夹

  双击打开即可，注意要配置环境变量！


###MAT 需要 JDK11 才能运行

解决办法是，打开 MAT 的安装目录，有一个配置文件 MemoryAnalyzer.ini。打开这个文件，在文件中指定 JDK 版本即可。

新增配置：

> -vm D:/jdkPath/bin/javaw.exe


###Detail
![image.png](https://upload-images.jianshu.io/upload_images/13965490-f1fcdffbf71a7171.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###Top Consumers 饼图查看快照中的大对象信息

![image.png](https://upload-images.jianshu.io/upload_images/13965490-32f0efbb54748a6a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/13965490-6009313e51a9a5c6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)






###Leak Suspects分析内存泄漏
~~~
package com.gbm.cloud;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
public class Main {

    public static void main(String[] args) {
        Main main = new Main();
        while (true) {
            try {
                Thread.sleep(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            main.run();
        }
    }

    private void run() {
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < 10; i++) {
            executorService.execute(() -> {
                // do something...
            });
        }
    }
}
~~~
为了找出到底是哪些对象没能被回收，我们加上运行参数
-Xms20m -Xmx20m -XX:+PrintGC -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=heap.bin，意思是发生OOM时把堆内存信息dump出来。运行程序直至异常，于是得到heap.dump文件，然后我们借助eclipse的MAT插件来分析，如果没有安装需要先安装。

然后File->Open Heap Dump... ，然后选择刚才dump出来的文件，选择Leak Suspects

![图片](https://upload-images.jianshu.io/upload_images/13965490-01cd1c4bdbe83e21?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

MAT会列出所有可能发生内存泄漏的对象

![图片](https://upload-images.jianshu.io/upload_images/13965490-b889773dd6f2cd3b?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看到居然有21260个Thread对象，3386个ThreadPoolExecutor对象，如果你去看一下`java.util.concurrent.ThreadPoolExecutor`的源码，可以发现线程池为了复用线程，会不断地等待新的任务，线程也不会回收，需要调用其shutdown方法才能让线程池执行完任务后停止。

其实线程池定义成局部变量，好的做法是设置成单例。



###histogram  列举内存中对象存在的个数和大小 

这个视图中提供了多种方式来对对象进行分类，这里为了分析方便，我们选择按包名进行分类。  
下面再来解释下列名：  
- Object 该类在内存当中的对象个数 
- Shallow Heap 对象自身所占用的内存大小，不包括它所引用的对象的内存大小
- Retained Heap 该对象被垃圾回收器回收之后，会释放的内存大小 

我们再来看一下右键菜单选项：


###Dominator tree 
该视图会以占用总内存的百分比来列举所有实例对象，注意这个地方是对象而不是类了，这个视图是用来发现大内存对象的 


###Duplicate Classes
 该视图显示重复的类等信息
![image.png](https://upload-images.jianshu.io/upload_images/13965490-60cba2da8962075a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###MAT修改内存空间

分析堆转储文件需要消耗很多的堆空间，为了保证分析的效率和性能，在有条件的情况下，建议分配给 MAT 尽可能多的内存资源。两种方式分配内存资源给 MAT：

*   修改启动参数 MemoryAnalyzer.exe -vmargs -Xmx4g
*   编辑文件 MemoryAnalyzer.ini 添加 -vmargs – Xmx4g

