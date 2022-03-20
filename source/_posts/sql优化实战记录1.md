---
title: sql优化实战记录1.md
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
title: sql优化实战记录1.md
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
帮忙处理了个慢SQL的问题。

这个SQL是普米监控系统里自动生成的，看了下执行计划，也确实有优化调整的空间。

尝试新增一个联合索引后，执行效率确实有所提升。不过发现当WHERE条件值换成一个新的取值时，第一次执行总是比较慢。

作为一个有着丰富实战（踩坑）经验的老DBA，首先就想到了是因为buffer pool不足，导致更换条件后需要执行物理读，所以第一次总是比较慢。

检查了一下，确实如此，innodb_buffer_pool_size才设置为134MB，而且innodb_io_capacity也是默认的200，好坑啊。

又看了下版本，还在使用MariaDB 5.5，这也太古董了吧。

.....
古人诚不我欺也，专业的事，还是让专业的人去做吧。突然想到了某位群友对DBA嗤之以鼻，认为现在都是上云时代，只要花钱加机器提高配置，什么都好办，不需要DBA一样耍的飞起。
......
