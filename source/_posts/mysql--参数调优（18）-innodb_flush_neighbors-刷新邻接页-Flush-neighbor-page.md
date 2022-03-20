---
title: mysql--参数调优（18）-innodb_flush_neighbors-刷新邻接页-Flush-neighbor-page.md
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
title: mysql--参数调优（18）-innodb_flush_neighbors-刷新邻接页-Flush-neighbor-page.md
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
innodb_flush_neighbors 参数是InnoDB用来控制buffer pool刷脏页时是否把脏页邻近的其他脏页一起刷到磁盘，在传统的机械硬盘时代，打开这个参数能够减少磁盘寻道的开销，显著提升性能。




取值范围：0，1，2 ； 默认值：5.7版本为1， 8.0版本为0

含义：
设置为0时，表示刷脏页时不刷其附近的脏页。
设置为1时，表示刷脏页时连带其附近毗连的脏页一起刷掉。
设置为2时，表示刷脏页时连带其附近区域的脏页一起刷掉。1与2的区别是2刷的区域更大一些。



推荐设置：
>机械硬盘设为1；SSD设为0

如果MySQL服务器磁盘是传统的HDD存储设备，打开该参数，能够减少I/O磁盘寻道的开销，提高性能，而对于SSD设备，寻道时间的性能影响很小，关闭该参数，反而能够分散写操作，提高数据库性能。由于SSD设备的普及，MySQL 8.0 将该参数的默认值由1调整为0。

目前在SSD盛行的情况下我们都把它设为0（不开启），如果你设置成了1即开启（默认状态）InnoDB就会额外地刷neighbors（刷新邻接脏页），因为SSD上的随机IO性能好不需要额外开销，所以不需要启用该特性。


配置实例：
~~~
[mysqld]
innodb_flush_neighbors = 0
~~~


Flush neighbor page 的影响
1、对于insert频繁的系统，这个功能比较适合
2、对于update频繁的系统，这个功能可能会带来一些副作用
- update顺带着刷新其他页；
- 对于update频繁的表，这些页马上就脏了，白白浪费写负载。


下面给出一段mysql5.7源码编译前程序员看的readme里的一句话：
This new default changes MySQL to cater for SSDs and fast storage devices by default. We expect that for the majority of users, this will result in a small performance gain. Users who are using slower hard drives may see a performance loss, and are encouraged to revert to the previous defaults by setting innodb_flush_neighbors=1.
