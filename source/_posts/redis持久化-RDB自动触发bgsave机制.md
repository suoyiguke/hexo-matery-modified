---
title: redis持久化-RDB自动触发bgsave机制.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
---
title: redis持久化-RDB自动触发bgsave机制.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: redis
categories: redis
---
引用：
https://mp.weixin.qq.com/s?__biz=MzI4NTA1MDEwNg==&mid=2650769300&idx=1&sn=49a11efa1a6ee605fceaddf240a55c40&chksm=f3f93201c48ebb175fa76053d95e315b621485b0e65e42d8b41fe91b8f859c9278f3adec7ca9&scene=21#wechat_redirect


### save m n

自动触发最常见的情况是在配置文件中通过save m n，指定当m秒内发生n次变化时，会触发bgsave。

例如，查看Redis的默认配置文件(Linux下为Redis根目录下的redis.conf)，可以看到如下配置信息：

![image](https://upload-images.jianshu.io/upload_images/13965490-0608750d3a6bde54?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

其中save 900 1的含义是：当时间到900秒时，如果Redis数据发生了至少1次变化，则执行bgsave；save 300 10和save 60 10000同理。当三个save条件满足任意一个时，都会引起bgsave的调用。

####save m n的实现原理

Redis的save m n，是通过serverCron函数、dirty计数器、和lastsave时间戳来实现的。

serverCron是Redis服务器的周期性操作函数，默认每隔100ms执行一次；该函数对服务器的状态进行维护，其中一项工作就是检查 save m n 配置的条件是否满足，如果满足就执行bgsave。

dirty计数器是Redis服务器维持的一个状态，记录了上一次执行bgsave/save命令后，服务器状态进行了多少次修改(包括增删改)；而当save/bgsave执行完成后，会将dirty重新置为0。

例如，如果Redis执行了set mykey helloworld，则dirty值会+1；如果执行了sadd myset v1 v2 v3，则dirty值会+3；注意dirty记录的是服务器进行了多少次修改，而不是客户端执行了多少修改数据的命令。

lastsave时间戳也是Redis服务器维持的一个状态，记录的是上一次成功执行save/bgsave的时间。

save m n的原理如下：每隔100ms，执行serverCron函数；在serverCron函数中，遍历save m n配置的保存条件，只要有一个条件满足，就进行bgsave。对于每一个save m n条件，只有下面两条同时满足时才算满足：

*   当前时间-lastsave > m

*   dirty >= n

save m n 执行日志

下图是save m n触发bgsave执行时，服务器打印日志的情况：


![image.png](https://upload-images.jianshu.io/upload_images/13965490-5d722c341456005f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###其他自动触发机制

除了save m n以外，还有一些其他情况会触发bgsave：

*   在主从复制场景下，如果从节点执行全量复制操作，则主节点会执行bgsave命令，并将rdb文件发送给从节点；

*   执行shutdown命令时，自动执行rdb持久化，如下图所示：
![image.png](https://upload-images.jianshu.io/upload_images/13965490-b94d08f4e095e7fa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/13965490-f9fe00218358d26b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

###bgsave的执行流程

前面介绍了触发bgsave的条件，下面将说明bgsave命令的执行流程，如下图所示：

![image](https://upload-images.jianshu.io/upload_images/13965490-75efe9e660c0f6a9?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


图片中的5个步骤所进行的操作如下：

*   Redis父进程首先判断：当前是否在执行save，或bgsave/bgrewriteaof（aof文件重写命令）的子进程，如果在执行则bgsave命令直接返回。bgsave/bgrewriteaof 的子进程不能同时执行，主要是基于性能方面的考虑：两个并发的子进程同时执行大量的磁盘写操作，可能引起严重的性能问题。

*   父进程执行fork操作创建子进程，这个过程中父进程是阻塞的，Redis不能执行来自客户端的任何命令；

*   父进程fork后，bgsave命令返回”Background saving started”信息并不再阻塞父进程，并可以响应其他命令；

*   子进程创建RDB文件，根据父进程内存快照生成临时快照文件，完成后对原有文件进行原子替换；

*   子进程发送信号给父进程表示完成，父进程更新统计信息。
