---
title: mysql-参数调优(4)之innodb的数据文件及redo-log的打开、刷写模式设置innodb_flush_method.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
---
title: mysql-参数调优(4)之innodb的数据文件及redo-log的打开、刷写模式设置innodb_flush_method.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql运维操作
categories: mysql运维操作
---
innodb_flush_method 可以对 innodb的数据文件及redo log的打开、刷写模式设置

这种偏理论的东西还是看官方文档实在。找再多博客也没用的。然后进下实验，理论联系
https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html

>文件的写入可以分为三个步骤： open、write（写入操作系统缓存）、flash（刷新到磁盘）



将innodb_flush_method设置为O_DIRECT以避免双重缓冲(InnoDB缓冲池和OS缓存同时使用)。唯一一种情况你不应该使用O_DIRECT是当你操作系统不支持时。但如果你运行的是Linux，使用O_DIRECT来激活直接IO。`windows 不支持O_DIRECT`

不用直接IO，双重缓冲将会发生，因为所有的数据库更改首先会写入到OS缓存然后才同步到硬盘 – 所以InnoDB缓冲池和OS缓存会同时持有一份相同的数据。特别是如果你的缓冲池限制为总内存的50%，那意味着在写密集的环境中你可能会浪费高达50%的内存。如果没有限制为50%，服务器可能由于OS缓存的高压力会使用到swap(交换空间，在windows下叫做虚拟内存。一般不得不使用虚拟内存时会导致性能变差，毕竟虚拟内存是由磁盘实现)。
 
>简单地说，设置为innodb_flush_method=O_DIRECT。


如果不配，它的默认值为fsync。

配置实例：
~~~
[mysqld]
innodb_flush_method = O_DIRECT
~~~


