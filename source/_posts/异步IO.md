---
title: 异步IO.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 操作系统
categories: 操作系统
---
---
title: 异步IO.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: 操作系统
categories: 操作系统
---
二、异步IO功能

1、关于AIO与SIO

　　为了提高磁盘操作性能，当前的数据库系统都采用异步IO的方式来处理磁盘操作。

　　1、异步IO：用户可以在发出一个IO请求后立即再发出另外一个IO请求，当全部IO请求发送完毕后，等待所有IO操作完成，这就是AIO。

　　2、与AIO对应的是Sync IO，即每进行一次IO操作，需要等待此次操作结束才能继续接下来的操作。

2、开启异步IO

　　首先OS要有异步io，且开启，然后mysqld要链接，要不然OS异步io没有开启，数据库的异步io也起不来。（this variable applies to Linux systems only, and cannot be changed while the server is running.）

　　1、文件系统层面需要打开这个功能：一般都是默认开启的。

<pre style="box-sizing: border-box; outline: 0px; margin: 0px; padding: 0px; font-weight: normal; position: relative; white-space: pre-wrap; overflow-wrap: break-word; overflow-x: auto; font-family: &quot;Courier New&quot; !important; font-size: 14px; line-height: 22px; color: rgb(0, 0, 0);">[root@localhost /]# ldconfig -v|grep libaio
    libaio.so.1.0.0 -> libaio.so.1.0.0 libaio.so.1 -> libaio.so.1.0.1</pre>

　　2、AIO是数据库层面的一个特性需要打开：默认是开启，开启的native aio性能提升，可以提高到75%。

![复制代码](https://upload-images.jianshu.io/upload_images/13965490-3f6512f67ea49858.gif?imageMogr2/auto-orient/strip) 

<pre style="box-sizing: border-box; outline: 0px; margin: 0px; padding: 0px; font-weight: normal; position: relative; white-space: pre-wrap; overflow-wrap: break-word; overflow-x: auto; font-family: &quot;Courier New&quot; !important; font-size: 14px; line-height: 22px; color: rgb(0, 0, 0);">mysql> show variables like 'innodb_use_native_aio'; +-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| innodb_use_native_aio | ON    |
+-----------------------+-------+
**1** row in set (**0.00** sec)</pre>

![复制代码](https://upload-images.jianshu.io/upload_images/13965490-7089938db3c2b065.gif?imageMogr2/auto-orient/strip) 

3、异步IO的好处　　

　　1、不用等待直接响应上一个用户的请求；

　　2、多次的请求在一起排序，请求的数据页是在一起的，一次读出来，减少多次读。（数据库的读写请求队列放在文件系统中单独分配的一块小内存结构里，非文件系统的缓存）

![image](https://upload-images.jianshu.io/upload_images/13965490-999b2e68da841726.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) 

4、wio：wait io

　　1、同步IO一定会产生wait IO

　　2、异步IO会降低wait IO，但是也可能会有wait IO

　　3、尽量采用异步IO(性能高于同步IO)

　　4、数据库层面启用异步IO

　　5、文件系统层面启用异步IO，Linux具备异步IO的能力

　　6、操作系统层面wio的含义理解

![复制代码](https://upload-images.jianshu.io/upload_images/13965490-a1ca6049e68148e8.gif?imageMogr2/auto-orient/strip) 

<pre style="box-sizing: border-box; outline: 0px; margin: 0px; padding: 0px; font-weight: normal; position: relative; white-space: pre-wrap; overflow-wrap: break-word; overflow-x: auto; font-family: &quot;Courier New&quot; !important; font-size: 14px; line-height: 22px; color: rgb(0, 0, 0);">[root@localhost /]# sar 1 Linux 2.6.32-431.el6.x86_64 (one)     07/14/2017     _x86_64_    (6 CPU) 04:23:25 AM     CPU     %user     %nice   %system   %iowait    %steal     %idle 04:23:26 AM     all      0.17      0.00      0.33      0.00      0.00     99.50
04:23:27 AM     all      0.00      0.00      1.00      0.00      0.00     99.00
^C
[root@localhost /]# iostat 1 Linux 2.6.32-431.el6.x86_64 (one)     07/14/2017     _x86_64_    (6 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle 0.00    0.00    0.02    0.02    0.00   99.96 Device:            tps   Blk_read/s   Blk_wrtn/s   Blk_read   Blk_wrtn
sda 0.26         6.70         4.07     619320     376232 scd0 0.00         0.00         0.00        352          0</pre>

![复制代码](https://upload-images.jianshu.io/upload_images/13965490-e9224c0ee2aa467e.gif?imageMogr2/auto-orient/strip) 

　　说明进程或是线程等待io的时间，值最好是小于5，大于25一定是io有问题。

在InnoDB存储引擎中，read ahead方式的读取都是通过AIO完成，脏页的刷新，也是通过AIO完成。
