---
title: mysql-主键设计.md
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
title: mysql-主键设计.md
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
###自增主键

优点
1、数据库自动编号，速度快，而且是增量增长，聚集型主键按顺序存放，对于检索非常有利。
2、数字型，占用空间小，易排序，在程序中传递方便。

缺点：
1、不支持水平分库，这种方法显然不能保证全局唯一。需要采取其它的一些手段。
2、高并发写下，对最大id的争用问题。使用表锁，InnoDb 5.1.22版本,为了解决自增主键锁表的问题，引入了参数innodb_autoinc_lock_mode。
3、暴露业务，比如可以通过一个月内注册用户的id的差值得到系统这个月内的新增用户数量，这种情况可以在弄一个uuid作为业务的id。加上唯一索引返回给调用者。
###UUID

优点： 
1、全局唯一性、安全性、可移植性。
2、能够保证独立性，程序可以在不同的数据库间迁移
3、 保证生成的ID不仅是表独立的，而且是库独立的，在你切分数据库的时候尤为重要

缺点： 
1、针对InnoDB引擎会徒增IO压力，InnoDB为聚集主键类型的引擎，数据会按照主键进行排序，由于UUID的无序性，InnoDB会产生巨大的IO压力。InnoDB主键索引和数据存储位置相关（簇类索引），uuid 主键可能会引起数据位置频繁变动，严重影响性能。
2、UUID长度过长，一个UUID占用128个比特（16个字节）。主键索引KeyLength长度过大，而影响能够基于内存的索引记录数量，进而影响基于内存的索引命中率，而基于硬盘进行索引查询性能很差。严重影响数据库服务器整体的性能表现。


![image.png](https://upload-images.jianshu.io/upload_images/13965490-d807f940cec67c7c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>UUID有全局唯一性，在游戏行业用的较多。比如“合服”将两个表的数据合并为一个表。这样就会很方便。如果是bigint自增类型那就不行了。

mysql8.0的uuid()可以优化为16个字节。
~~~
(root@localhost) [(none)]>SELECT  length(UUID_TO_BIN(uuid()));
+-----------------------------+
| length(UUID_TO_BIN(uuid())) |
+-----------------------------+
|                          16 |
+-----------------------------+
1 row in set (0.00 sec)

(root@localhost) [(none)]>SELECT  length(uuid());
+----------------+
| length(uuid()) |
+----------------+
|             36 |

~~~
 
