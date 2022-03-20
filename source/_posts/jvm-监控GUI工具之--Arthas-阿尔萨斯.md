---
title: jvm-监控GUI工具之--Arthas-阿尔萨斯.md
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
title: jvm-监控GUI工具之--Arthas-阿尔萨斯.md
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


上述的GUI诊断工具不利于在生产环境使用

官方文档: [https://arthas.aliyun.com/doc](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc)

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E4%B8%8B%E8%BD%BD%E5%B9%B6%E4%BD%BF%E7%94%A8)下载并使用

在Linux中

<pre style="box-sizing: border-box; overflow: auto; font-family: SFMono-Regular, Menlo, Monaco, Consolas, &quot;Liberation Mono&quot;, &quot;Courier New&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; line-height: 1.45; background-color: rgb(246, 248, 250); border-radius: 3px; word-break: normal; min-height: 52px; tab-size: 4; color: rgb(51, 51, 51);">#下载
curl -O https://arthas.aliyun.com/arthas-boot.jar</pre>

![image-20210521162643459](https://upload-images.jianshu.io/upload_images/13965490-e8c112b8793533b2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

随便启动一个Java程序再启动arthas分析

<pre style="box-sizing: border-box; overflow: auto; font-family: SFMono-Regular, Menlo, Monaco, Consolas, &quot;Liberation Mono&quot;, &quot;Courier New&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; line-height: 1.45; background-color: rgb(246, 248, 250); border-radius: 3px; word-break: normal; min-height: 52px; tab-size: 4; color: rgb(51, 51, 51);">#启动
java -jar arthas-boot.jar</pre>

![image-20210521162916782](https://upload-images.jianshu.io/upload_images/13965490-4cf761b3f8182e39.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

<pre style="box-sizing: border-box; overflow: auto; font-family: SFMono-Regular, Menlo, Monaco, Consolas, &quot;Liberation Mono&quot;, &quot;Courier New&quot;, monospace; font-size: 13.6px; margin-top: 0px; margin-bottom: 0px; overflow-wrap: normal; padding: 16px; line-height: 1.45; background-color: rgb(246, 248, 250); border-radius: 3px; word-break: normal; min-height: 52px; tab-size: 4; color: rgb(51, 51, 51);">#关闭服务器(关闭所有客户端)
stop

#关闭当前客户端
quit</pre>

![image-20210521195844113](https://upload-images.jianshu.io/upload_images/13965490-260097f0bf204660.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#%E5%9F%BA%E7%A1%80%E5%91%BD%E4%BB%A4)基础命令

*   help——查看命令帮助信息
*   [cat](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fcat.html)——打印文件内容，和linux里的cat命令类似
*   [echo](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fecho.html)–打印参数，和linux里的echo命令类似
*   [grep](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fgrep.html)——匹配查找，和linux里的grep命令类似
*   [base64](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fbase64.html)——base64编码转换，和linux里的base64命令类似
*   [tee](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Ftee.html)——复制标准输入到标准输出和指定的文件，和linux里的tee命令类似
*   [pwd](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fpwd.html)——返回当前的工作目录，和linux命令类似
*   cls——清空当前屏幕区域
*   session——查看当前会话的信息
*   [reset](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Freset.html)——重置增强类，将被 Arthas 增强过的类全部还原，Arthas 服务端关闭时会重置所有增强过的类
*   version——输出当前目标 Java 进程所加载的 Arthas 版本号
*   history——打印命令历史
*   quit——退出当前 Arthas 客户端，其他 Arthas 客户端不受影响
*   stop——关闭 Arthas 服务端，所有 Arthas 客户端全部退出
*   [keymap](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fkeymap.html)——Arthas快捷键列表及自定义快捷键

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#jvm%E7%9B%B8%E5%85%B3)jvm相关

*   [dashboard](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fdashboard.html)——当前系统的实时数据面板
*   [thread](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fthread.html)——查看当前 JVM 的线程堆栈信息
*   [jvm](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fjvm.html)——查看当前 JVM 的信息
*   [sysprop](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fsysprop.html)——查看和修改JVM的系统属性
*   [sysenv](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fsysenv.html)——查看JVM的环境变量
*   [vmoption](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fvmoption.html)——查看和修改JVM里诊断相关的option
*   [perfcounter](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fperfcounter.html)——查看当前 JVM 的Perf Counter信息
*   [logger](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Flogger.html)——查看和修改logger
*   [getstatic](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fgetstatic.html)——查看类的静态属性
*   [ognl](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fognl.html)——执行ognl表达式
*   [mbean](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fmbean.html)——查看 Mbean 的信息
*   [heapdump](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fheapdump.html)——dump java heap, 类似jmap命令的heap dump功能
*   [vmtool](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fvmtool.html)——从jvm里查询对象，执行forceGc

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#classclassloader%E7%9B%B8%E5%85%B3)class/classloader相关

*   [sc](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fsc.html)——查看JVM已加载的类信息
*   [sm](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fsm.html)——查看已加载类的方法信息
*   [jad](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fjad.html)——反编译指定已加载类的源码
*   [mc](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fmc.html)——内存编译器，内存编译`.java`文件为`.class`文件
*   [retransform](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fretransform.html)——加载外部的`.class`文件，retransform到JVM里
*   [redefine](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fredefine.html)——加载外部的`.class`文件，redefine到JVM里
*   [dump](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fdump.html)——dump 已加载类的 byte code 到特定目录
*   [classloader](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fclassloader.html)——查看classloader的继承树，urls，类加载信息，使用classloader去getResource

#### [](https://gitee.com/tcl192243051/studyJVM/blob/master/4_%E6%80%A7%E8%83%BD%E8%B0%83%E4%BC%98%E7%AF%87/JVM%E7%9B%91%E6%8E%A7%E5%8F%8A%E8%AF%8A%E6%96%AD%E5%B7%A5%E5%85%B7-GUI%E7%AF%87.md#monitorwatchtrace%E7%9B%B8%E5%85%B3)monitor/watch/trace相关

> 请注意，这些命令，都通过字节码增强技术来实现的，会在指定类的方法中插入一些切面来实现数据统计和观测，因此在线上、预发使用时，请尽量明确需要观测的类、方法以及条件，诊断结束要执行 `stop` 或将增强过的类执行 `reset` 命令。

*   [monitor](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fmonitor.html)——方法执行监控
*   [watch](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fwatch.html)——方法执行数据观测
*   [trace](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Ftrace.html)——方法内部调用路径，并输出方法路径上的每个节点上耗时
*   [stack](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Fstack.html)——输出当前方法被调用的调用路径
*   [tt](https://gitee.com/link?target=https%3A%2F%2Farthas.aliyun.com%2Fdoc%2Ftt.html)——方法执行数据的时空隧道，记录下指定方法每次调用的入参和返回信息，并能对这些不同的时间下调用进行观测
