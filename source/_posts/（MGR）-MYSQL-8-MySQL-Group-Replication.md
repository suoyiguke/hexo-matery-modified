---
title: （MGR）-MYSQL-8-MySQL-Group-Replication.md
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
title: （MGR）-MYSQL-8-MySQL-Group-Replication.md
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

###什么是MySQL MGR
MySQL Group Replication（MGR）是以插件形式存在的，MySQL MGR用来解决一个数据库高可用与高扩展的解决方案，MGR是从MySQL 5.7.17版本推出的。

MySQL MGR基于分布式paxos协议来实现组复制，用以保证数据一致性。MGR内置故障检测和自动选主功能，只要不是集群中的大多数节点都宕机，就可以继续正常工作。




1、知乎专栏- 网易杭州 MGR
2、腾讯课堂
3、

![image.png](https://upload-images.jianshu.io/upload_images/13965490-7da82db57005b091.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


MySQL Group Replication（简称MGR）字面意思是mysql组复制的意思,但其实他是一个高可用的集群架构,暂时只支持mysql5.7和mysql8.0版本. 推荐使用mysql8.0版本，5.7会有很多坑


**ROW-base 异步复制**

![image.png](https://upload-images.jianshu.io/upload_images/13965490-9a71e4f9616fc7e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**半同步复制**
![image.png](https://upload-images.jianshu.io/upload_images/13965490-c5a4bad00b4aba23.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**MRG**

多节点投票 保证数据一致









**MRG**

3 5  7 9
