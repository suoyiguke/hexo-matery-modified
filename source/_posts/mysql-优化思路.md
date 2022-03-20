---
title: mysql-优化思路.md
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
title: mysql-优化思路.md
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


分区、分表、分库
读写分离、集群

###大方向
1、如果确实用的是单数据库，那么优化最先从数据库索引、分区、参数配置这块入手


2、如果数据量确实大，并发量大，那就是基于以上操作，进行分库分表。
读写分离、主从复制

3、缓存

###优化问题
1、表关联多，表的设计有缺陷
2、索引没优化
3、语句没优化
4、调优服务器参数：
缓冲区，线程数量等
5、表、字段、设计上的优化
###优化流程


![image.png](https://upload-images.jianshu.io/upload_images/13965490-2da13f2a1d993ac3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

