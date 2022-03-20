---
title: OOM-killer.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
---
title: OOM-killer.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: linux
categories: linux
---
# [ux进程被杀掉（OOM killer），查看系统日志](https://www.cnblogs.com/duanxz/p/10185946.html)

**基本概念：**

Linux 内核有个机制叫OOM killer(Out Of Memory killer)，该机制会监控那些占用内存过大，尤其是瞬间占用内存很快的进程，然后防止内存耗尽而自动把该进程杀掉。内核检测到系统内存不足、挑选并杀掉某个进程的过程可以参考内核源代码linux/mm/oom_kill.c，当系统内存不足的时候，out_of_memory()被触发，然后调用select_bad_process()选择一个”bad”进程杀掉。如何判断和选择一个”bad进程呢？linux选择”bad”进程是通过调用oom_badness()，挑选的算法和想法都很简单很朴实：最bad的那个进程就是那个最占用内存的进程。

**如何查看：**

grep "Out of memory" /var/log/messages

![image](https://upload-images.jianshu.io/upload_images/13965490-01702b2fad8d0dce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

查看系统日志方法：

运行egrep -i -r 'killed process' /var/log命令，结果如下：

![image](https://upload-images.jianshu.io/upload_images/13965490-43599ab868e76e24.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

也可运行dmesg命令，结果如下：

![image](https://upload-images.jianshu.io/upload_images/13965490-607d6beb6b9060da.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
