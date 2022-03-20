---
title: mysql-主从同步延迟问题.md
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
title: mysql-主从同步延迟问题.md
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

### 从数据库的读的延迟问题了解吗？如何解决？

mysql压力小，延迟自然会变小。
- 架构方面

服务的基础架构在业务和mysql之间加入memcache或者redis的cache层。降低mysql的读压力。


- 硬件方面

1、采用好服务器，比如4核比2核性能明显好，2核比1核性能明显好。
2、存储用ssd，提升随机写的性能。
3、主从间保证处在同一个交换机下面，并且是万兆环境。
总结，硬件强劲，延迟自然会变小。一句话，缩小延迟的解决方案就是花钱和花时间。

- mysql主从同步加速

1、sync_binlog在slave端设置为0
2、–logs-slave-updates 从服务器从主服务器接收到的更新不记入它的二进制日志。
3、直接禁用slave端的binlog
4、slave端，如果使用的存储引擎是innodb，innodb_flush_log_at_trx_commit =2


### 做主从后主服务器挂了怎么办？

###
~~~
1007：数据库已存在，创建数据库失败
1008：数据库不存在，删除数据库失败
1050：数据表已存在，创建数据表失败
1050：数据表不存在，删除数据表失败
1054：字段不存在，或程序文件跟数据库有冲突
1060：字段重复，导致无法插入
1061：重复键名
1068：定义了多个主键
1094：位置线程ID
1146：数据表缺失，请恢复数据库
~~~
