---
title: mysql-主从复制日常维护工作2--查看主从复制的进度.md
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
title: mysql-主从复制日常维护工作2--查看主从复制的进度.md
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
很多情况下，我们都想知道从库复制的进度如何。知道这个差距，可以帮助我们判断是否需要手工来做主从的同步工作，也可以帮助我们判断从库上做统计的数据精度如何。这个值可以通过SHOW PROCESSLIST 列表中的Slave_SQL_Running线程的Time值得到，它记录了从库当前执行的SQL时间戳与系统时间之间的差距，单位是秒。

如下，在从库中执行。得到IO线程的time是57512秒也就是15小时。最后执行的复制操作大概是主库上15小时之前的更新了。
~~~
mysql> SHOW PROCESSLIST;
+----+-------------+-----------------+------+---------+-------+--------------------------------------------------------+------------------+
| Id | User        | Host            | db   | Command | Time  | State                                                  | Info             |
+----+-------------+-----------------+------+---------+-------+--------------------------------------------------------+------------------+
| 25 | system user |                 | NULL | Connect | 57512 | Waiting for master to send event                       | NULL             |
| 26 | system user |                 | NULL | Connect | 57571 | Slave has read all relay log; waiting for more updates | NULL             |
| 28 | root        | localhost:58816 | test | Query   |     0 | starting                                               | SHOW PROCESSLIST |
| 29 | root        | localhost:58818 | test | Sleep   |    10 |                                                        | NULL             |
| 30 | root        | localhost:58820 | test | Sleep   |    10 |                                                        | NULL             |
+----+-------------+-----------------+------+---------+-------+--------------------------------------------------------+------------------+
5 rows in set (0.02 sec)
~~~

下面通过例子测试一下这个时间的准确性。
