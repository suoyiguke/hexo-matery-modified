---
title: mysql-单表到此能多少条数据？.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
---
title: mysql-单表到此能多少条数据？.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: mysql基本
categories: mysql基本
---
首先在oracle中根本没有说一张表超过了500万就要分表的说法，想存多少就存多少好吗！

###那么在mysql中为啥有这个说法呢？

基本上有两个原因：
1、 DDL 创建索引时会创建表锁。
如果一个表数据太大，比如有一千万。在线上大表里添加字段或者添加索引时这样锁的时间太长了。
对于管理上来看也算是分表的一个理由。因为之前不支持online ddl，但是现在就不同了。

2、在mysql索引实现上的却是有一把大锁。但是对这个性能影响不大，特别是在mysql5.7时已经解决。


###用mysql一定要用SSD
使用SSD的的话mysql单表1个亿的数据没有太大的问题。SASS的IOPS只有1000。SASS的话500万一张表才差不多。
>说数据量太大要分表都是几年钱的思想。现在的SSD很便宜，500G才5K。


网易MySQL单个库，500G左右，最大1T以上。


###分区表不提升性能
分区表只是便于管理，对性能没有作用，用了只会让性能下降。
