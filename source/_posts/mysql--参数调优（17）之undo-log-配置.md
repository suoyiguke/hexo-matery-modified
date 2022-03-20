---
title: mysql--参数调优（17）之undo-log-配置.md
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
title: mysql--参数调优（17）之undo-log-配置.md
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
**innodb_undo_directory = /undolog/**

这个就不用解释了，太傻瓜了。这种路径的都可由运维决定，记得挂在大磁盘下。

**innodb_undo_logs = 128**

推荐设置：128
作用：指定回滚段的个数（早期版本该参数名字是innodb_rollback_segments），默认128个。每个回滚段可同时支持1024个在线事务。这些回滚段会平均分布到各个undo表空间中。该变量可以动态调整，但是物理上的回滚段不会减少，只是会控制用到的回滚段的个数。现在SSD非常普及。innodb_undo_logs可以默认为128不变。如果不配的后果：默认就是128
配置实例：
~~~
[mysqld]
innodb_undo_logs = 128
~~~
**innodb_undo_tablespaces**
推荐：3，默认为3
作用：
定单独存放的undo表空间个数，例如如果设置为3，则undo表空间为undo001、undo002、undo003，每个文件初始大小默认为10M。该参数我们推荐设置为大于等于3，更多的碎片文件会影响磁盘的io性能，而不够碎片同样影响mysql的吞吐率，在ssd上一般最佳的配置在3.如果只有1个undo表空间，那么整个系统在此过程中将处于不可用状态。为了尽可能降低truncate对系统的影响，建议将该参数最少设置为3；
如果不配的后果：默认为：3
配置实例：
~~~
[mysqld]
innodb_undo_tablespaces = 3
~~~

**innodb_flush_neighbors**

推荐设置：
>机械硬盘设为1；SSD设为0

作用：这个参数很要紧，目前在ssd盛行的情况下我们都把它设为0（不开启），如果你设置成了1即开启（默认状态）InnoDB就会刷新一个extent中的所有页面，因为SSD在随机IO上没有额外负载，所以不需要启用该特性，开启了反而多此一句。下面给出一段mysql5.7源码编译前程序员看的readme里的一句话：

This new default changes MySQL to cater for SSDs and fast storage devices by default. We expect that for the majority of users, this will result in a small performance gain. Users who are using slower hard drives may see a performance loss, and are encouraged to revert to the previous defaults by setting innodb_flush_neighbors=1.

如果不配的后果：它的默认是1，不是0.这个参数对机性硬盘来说很有效，可以减少随机io，增加性能。如果是ssd类磁盘，建议设置为0，可以更快的刷新脏页。如果你把它设为1同时又是ssd那就显得没必要了。这边普及一下小知识，如果你装过8.0，你可以去看一下，8.0已经把这个默认值设为0了。

配置实例：
~~~
[mysqld]
innodb_flush_neighbors = 0
~~~
